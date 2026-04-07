(function () {
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  var yearEl = document.getElementById("year");
  var mqMobileNav = window.matchMedia("(max-width: 768px)");

  function isMobileNavLayout() {
    return mqMobileNav.matches;
  }

  function resetNavDropdowns() {
    if (!header) return;
    header.querySelectorAll(".nav__item--dropdown").forEach(function (li) {
      li.classList.remove("is-submenu-open");
    });
    header.querySelectorAll(".nav__link--has-sub").forEach(function (t) {
      t.setAttribute("aria-expanded", "false");
    });
  }

  function closeMobileNav() {
    if (!header || !toggle) return;
    header.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    resetNavDropdowns();
  }

  if (yearEl) {
    yearEl.textContent = String(new Date().getFullYear());
  }

  if (toggle && header) {
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (!open) {
        resetNavDropdowns();
      }
    });

    header.querySelectorAll(".nav a").forEach(function (link) {
      link.addEventListener("click", function () {
        if (isMobileNavLayout() && link.classList.contains("nav__link--has-sub")) {
          return;
        }
        closeMobileNav();
      });
    });
  }

  document.querySelectorAll(".js-home-top").forEach(function (a) {
    a.addEventListener("click", function (e) {
      if (!document.body.classList.contains("is-home")) return;
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
      try {
        history.replaceState(null, "", window.location.pathname + window.location.search);
      } catch (err) {}
      closeMobileNav();
    });
  });

  document.querySelectorAll(".nav__item--dropdown > .nav__link--has-sub").forEach(function (trigger) {
    trigger.addEventListener("click", function (e) {
      if (isMobileNavLayout()) {
        e.preventDefault();
        var item = trigger.closest(".nav__item--dropdown");
        if (!item) return;
        var willOpen = !item.classList.contains("is-submenu-open");
        document.querySelectorAll(".nav__item--dropdown.is-submenu-open").forEach(function (other) {
          if (other !== item) {
            other.classList.remove("is-submenu-open");
            var t = other.querySelector(":scope > .nav__link--has-sub");
            if (t) t.setAttribute("aria-expanded", "false");
          }
        });
        item.classList.toggle("is-submenu-open", willOpen);
        trigger.setAttribute("aria-expanded", willOpen ? "true" : "false");
        return;
      }
      if (trigger.getAttribute("href") === "#") {
        e.preventDefault();
      }
    });
  });

  function bindAccordionTrigger(btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest(".faq-item") || btn.closest(".service-panel");
      var panelId = btn.getAttribute("aria-controls");
      var panel = panelId
        ? document.getElementById(panelId)
        : item && (item.querySelector(".faq-item__panel") || item.querySelector(".service-panel__panel"));
      var expanded = btn.getAttribute("aria-expanded") === "true";
      var next = !expanded;
      btn.setAttribute("aria-expanded", next ? "true" : "false");
      if (item) item.classList.toggle("is-open", next);
      if (panel) panel.setAttribute("aria-hidden", next ? "false" : "true");
    });
  }

  document.querySelectorAll(".faq-item__trigger").forEach(bindAccordionTrigger);
  document.querySelectorAll(".service-panel__trigger").forEach(bindAccordionTrigger);

  /* Referenciák + Rólam masonry: lightbox, lapozás, átlátszó háttér */
  (function refLightbox() {
    var modal = document.getElementById("ref-lightbox");
    if (!modal) return;

    var grids = document.querySelectorAll(".ref-grid, .rolam-masonry");
    if (!grids.length) return;

    var backdrop = modal.querySelector(".ref-lightbox__backdrop");
    var figure = modal.querySelector(".ref-lightbox__figure");
    var img = modal.querySelector(".ref-lightbox__img");
    var btnPrev = modal.querySelector(".ref-lightbox__prev");
    var btnNext = modal.querySelector(".ref-lightbox__next");
    var btnClose = modal.querySelector(".ref-lightbox__close");

    var items = [];
    var index = 0;
    var lastFocus = null;
    var touchStartX = 0;
    var onDocKey = null;

    function collectItemsFrom(grid) {
      items = [];
      Array.prototype.forEach.call(grid.querySelectorAll(".ref-grid__cell, .rolam-masonry__cell"), function (cell) {
        var el = cell.querySelector("img");
        if (el) {
          items.push({
            src: el.currentSrc || el.src,
            alt: el.getAttribute("alt") || "Referenciakép",
          });
        }
      });
    }

    function go(delta) {
      if (!items.length) return;
      index = (index + delta + items.length) % items.length;
      img.src = items[index].src;
      img.alt = items[index].alt;
    }

    function close() {
      if (onDocKey) {
        document.removeEventListener("keydown", onDocKey);
        onDocKey = null;
      }
      modal.setAttribute("hidden", "");
      modal.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
      img.removeAttribute("src");
      if (lastFocus && typeof lastFocus.focus === "function") {
        lastFocus.focus();
      }
    }

    function open(grid, at) {
      collectItemsFrom(grid);
      if (!items.length) return;
      index = at;
      if (index < 0) index = 0;
      if (index >= items.length) index = items.length - 1;
      lastFocus = document.activeElement;
      img.src = items[index].src;
      img.alt = items[index].alt;
      modal.removeAttribute("hidden");
      modal.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";

      onDocKey = function (e) {
        if (e.key === "Escape") {
          e.preventDefault();
          close();
        } else if (e.key === "ArrowLeft") {
          e.preventDefault();
          go(-1);
        } else if (e.key === "ArrowRight") {
          e.preventDefault();
          go(1);
        }
      };
      document.addEventListener("keydown", onDocKey);

      btnClose.focus();
    }

    Array.prototype.forEach.call(grids, function (grid) {
      grid.addEventListener("click", function (e) {
        var cell = e.target.closest(".ref-grid__cell") || e.target.closest(".rolam-masonry__cell");
        if (!cell || !grid.contains(cell)) return;
        var cells = grid.querySelectorAll(".ref-grid__cell, .rolam-masonry__cell");
        var i = Array.prototype.indexOf.call(cells, cell);
        if (i >= 0) open(grid, i);
      });
    });

    if (backdrop) backdrop.addEventListener("click", close);
    btnClose.addEventListener("click", close);
    btnPrev.addEventListener("click", function () {
      go(-1);
    });
    btnNext.addEventListener("click", function () {
      go(1);
    });

    if (figure) {
      figure.addEventListener(
        "touchstart",
        function (e) {
          touchStartX = e.changedTouches[0].screenX;
        },
        { passive: true }
      );
      figure.addEventListener(
        "touchend",
        function (e) {
          var x = e.changedTouches[0].screenX;
          var dx = x - touchStartX;
          if (Math.abs(dx) < 48) return;
          if (dx > 0) go(-1);
          else go(1);
        },
        { passive: true }
      );
    }
  })();

  /* Testimonials karousel: gap a diák között, translateX = i * (viewport + gap) px */
  (function testimonialsCarousel() {
    var root = document.querySelector("[data-testimonials-carousel]");
    if (!root) return;

    var viewport = root.querySelector(".testimonials-carousel__viewport");
    var track = root.querySelector(".testimonials-carousel__track");
    var slides = root.querySelectorAll(".testimonials-carousel__slide");
    var dots = root.querySelectorAll(".testimonials-carousel__dot");
    var n = slides.length;
    var i = 0;
    var timer = null;
    var intervalMs = 15000;
    var slideStepPx = 0;

    if (!track || !viewport || !n) return;

    function parseGapPx() {
      var cs = window.getComputedStyle(track);
      var g = cs.gap || cs.columnGap || "0";
      var parsed = parseFloat(g);
      return isNaN(parsed) ? 0 : parsed;
    }

    function measure() {
      var w = Math.round(viewport.getBoundingClientRect().width);
      if (w < 1) return;
      var gapPx = parseGapPx();
      slideStepPx = w + gapPx;
      slides.forEach(function (slide) {
        slide.style.flex = "0 0 " + w + "px";
        slide.style.width = w + "px";
        slide.style.maxWidth = w + "px";
        slide.style.minWidth = w + "px";
      });
      track.style.transform = "translateX(-" + Math.round(i * slideStepPx) + "px)";
    }

    function setAria() {
      slides.forEach(function (slide, idx) {
        slide.setAttribute("aria-hidden", idx !== i ? "true" : "false");
      });
      dots.forEach(function (dot, idx) {
        var on = idx === i;
        dot.classList.toggle("is-active", on);
        dot.setAttribute("aria-selected", on ? "true" : "false");
        dot.tabIndex = on ? 0 : -1;
      });
    }

    function go(to) {
      i = ((to % n) + n) % n;
      if (slideStepPx < 1) measure();
      track.style.transform = "translateX(-" + Math.round(i * slideStepPx) + "px)";
      setAria();
    }

    function next() {
      go(i + 1);
    }

    function stopAutoplay() {
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
    }

    function startAutoplay() {
      if (document.hidden) return;
      stopAutoplay();
      timer = setInterval(next, intervalMs);
    }

    dots.forEach(function (dot, idx) {
      dot.addEventListener("click", function () {
        go(idx);
        stopAutoplay();
        startAutoplay();
      });
    });

    root.addEventListener("mouseenter", stopAutoplay);
    root.addEventListener("mouseleave", startAutoplay);
    root.addEventListener("focusin", stopAutoplay);
    root.addEventListener("focusout", function (e) {
      if (!root.contains(e.relatedTarget)) startAutoplay();
    });

    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stopAutoplay();
      else startAutoplay();
    });

    var resizeT;
    window.addEventListener("resize", function () {
      clearTimeout(resizeT);
      resizeT = setTimeout(function () {
        measure();
      }, 80);
    });

    measure();
    setAria();
    startAutoplay();
  })();

  /* Aloldal: vízszintes előtte–utána galéria — pontok = lapozások száma, lassú animáció */
  (function pageGallery() {
    var root = document.querySelector("[data-page-gallery]");
    if (!root) return;

    var viewport = root.querySelector(".page-gallery__viewport");
    var prev = root.querySelector(".page-gallery__nav--prev");
    var next = root.querySelector(".page-gallery__nav--next");
    var dotsNav = root.querySelector("[data-page-gallery-dots]");
    if (!viewport || !prev || !next) return;

    var slides = viewport.querySelectorAll(".page-gallery__slide");
    var track = viewport.querySelector(".page-gallery__track");

    var dotsBuiltForPageCount = -1;
    var scrollAnimGen = 0;
    var SCROLL_MS = 700;
    var layoutDebounceTimer = null;

    function trackGap() {
      if (!track) return 0;
      var cs = window.getComputedStyle(track);
      var g = parseFloat(cs.columnGap || cs.gap || "0");
      return isNaN(g) ? 0 : g;
    }

    function stepWidth() {
      var slide = slides[0];
      if (!slide) return 0;
      return slide.getBoundingClientRect().width + trackGap();
    }

    function maxScrollLeft() {
      return Math.max(0, viewport.scrollWidth - viewport.clientWidth);
    }

    /** Hány dia fér el nagyjából egyszerre a nézetben */
    function visibleSlideCount() {
      var sw = stepWidth();
      if (!sw) return 1;
      var n = Math.floor(viewport.clientWidth / sw);
      return Math.max(1, Math.min(n, slides.length));
    }

    /** Lapozási pozíciók száma: első dia indexe 0 … utolsó, hogy a végén ne maradjon „üres” pont */
    function getPageCount() {
      if (!slides.length) return 0;
      var v = visibleSlideCount();
      return Math.max(1, slides.length - v + 1);
    }

    function easeInOutCubic(t) {
      return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    function prefersReducedMotion() {
      return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    }

    function finishScrollAnim() {
      viewport.classList.remove("page-gallery__viewport--animating");
      syncDots();
      syncNav();
    }

    function smoothScrollTo(targetLeft, duration) {
      var maxS = maxScrollLeft();
      targetLeft = Math.max(0, Math.min(targetLeft, maxS));
      if (prefersReducedMotion()) {
        viewport.scrollLeft = targetLeft;
        finishScrollAnim();
        return;
      }
      duration = duration != null ? duration : SCROLL_MS;
      scrollAnimGen += 1;
      var myGen = scrollAnimGen;
      var start = viewport.scrollLeft;
      var delta = targetLeft - start;
      if (Math.abs(delta) < 0.5) {
        finishScrollAnim();
        return;
      }
      viewport.classList.add("page-gallery__viewport--animating");
      var t0 = null;

      function tick(now) {
        if (myGen !== scrollAnimGen) {
          viewport.classList.remove("page-gallery__viewport--animating");
          return;
        }
        if (t0 === null) t0 = now;
        var elapsed = now - t0;
        var t = Math.min(1, elapsed / duration);
        viewport.scrollLeft = start + delta * easeInOutCubic(t);
        if (t < 1) requestAnimationFrame(tick);
        else finishScrollAnim();
      }
      requestAnimationFrame(tick);
    }

    function step(dir) {
      var sw = stepWidth();
      if (!sw) return;
      var maxS = maxScrollLeft();
      if (maxS < 8) return;
      var x = viewport.scrollLeft;
      var target;
      if (dir > 0) {
        target = x >= maxS - 4 ? 0 : Math.min(x + sw, maxS);
      } else {
        target = x <= 4 ? maxS : Math.max(x - sw, 0);
      }
      smoothScrollTo(target);
    }

    function goToPage(pageIndex) {
      var sw = stepWidth();
      if (!sw) return;
      var pages = getPageCount();
      var p = Math.max(0, Math.min(pageIndex, pages - 1));
      smoothScrollTo(p * sw);
    }

    function activePageIndex() {
      var sw = stepWidth();
      var pages = getPageCount();
      if (!sw || pages <= 1) return 0;
      var maxS = maxScrollLeft();
      var x = viewport.scrollLeft;
      if (x >= maxS - 3) return pages - 1;
      var idx = Math.round(x / sw);
      return Math.max(0, Math.min(idx, pages - 1));
    }

    function syncDots() {
      if (!dotsNav) return;
      var dots = dotsNav.querySelectorAll(".page-gallery__dot");
      if (!dots.length) return;
      var ai = activePageIndex();
      dots.forEach(function (d, i) {
        var on = i === ai;
        d.classList.toggle("is-active", on);
        if (on) d.setAttribute("aria-current", "true");
        else d.removeAttribute("aria-current");
      });
    }

    function syncNav() {
      if (!track) return;
      var vw = viewport.getBoundingClientRect().width;
      var tw = track.getBoundingClientRect().width;
      var maxS = maxScrollLeft();
      var canScroll = tw > vw + 8 || maxS > 8;
      if (!canScroll) {
        prev.disabled = true;
        next.disabled = true;
        prev.setAttribute("aria-disabled", "true");
        next.setAttribute("aria-disabled", "true");
        return;
      }
      /* Körkörös lapozás: a nyilak mindig aktívak, ha több oldal van */
      prev.disabled = false;
      next.disabled = false;
      prev.removeAttribute("aria-disabled");
      next.removeAttribute("aria-disabled");
    }

    function buildDots() {
      if (!dotsNav || !slides.length) return;
      var pages = getPageCount();
      dotsNav.innerHTML = "";
      for (var p = 0; p < pages; p++) {
        (function (page) {
          var b = document.createElement("button");
          b.type = "button";
          b.className = "page-gallery__dot";
          b.setAttribute("aria-label", page + 1 + ". oldal");
          b.addEventListener("click", function () {
            goToPage(page);
          });
          dotsNav.appendChild(b);
        })(p);
      }
      dotsBuiltForPageCount = pages;
    }

    function ensureDots() {
      if (!dotsNav || !slides.length) return;
      var pages = getPageCount();
      if (pages !== dotsBuiltForPageCount || dotsNav.children.length !== pages) {
        buildDots();
      }
    }

    function scheduleGallerySync() {
      window.requestAnimationFrame(function () {
        ensureDots();
        syncDots();
        syncNav();
      });
    }

    function debouncedLayoutSync() {
      if (layoutDebounceTimer) clearTimeout(layoutDebounceTimer);
      layoutDebounceTimer = setTimeout(function () {
        layoutDebounceTimer = null;
        window.requestAnimationFrame(function () {
          var pc = getPageCount();
          if (pc !== dotsBuiltForPageCount || dotsNav.children.length !== pc) {
            buildDots();
          }
          syncDots();
          syncNav();
        });
      }, 120);
    }

    var scrollTick = null;
    function onScroll() {
      if (scrollTick) return;
      scrollTick = window.requestAnimationFrame(function () {
        scrollTick = null;
        syncDots();
        syncNav();
      });
    }

    viewport.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", debouncedLayoutSync, { passive: true });

    window.addEventListener("load", scheduleGallerySync, { passive: true });

    if (typeof ResizeObserver !== "undefined") {
      var ro = new ResizeObserver(function () {
        debouncedLayoutSync();
      });
      ro.observe(viewport);
      if (track) ro.observe(track);
    }

    viewport.querySelectorAll("img").forEach(function (img) {
      if (img.complete) return;
      img.addEventListener("load", scheduleGallerySync, { passive: true });
      img.addEventListener("error", scheduleGallerySync, { passive: true });
    });

    prev.addEventListener("click", function () {
      step(-1);
    });
    next.addEventListener("click", function () {
      step(1);
    });

    scheduleGallerySync();
  })();

  /* Árlista táblák: oszlopfejléc → data-label (csak ár oszlopok; mobil) */
  (function initArlistaPriceTableLabels() {
    var root = document.querySelector(".arlista-content");
    if (!root) return;
    root.querySelectorAll(".price-table").forEach(function (table) {
      var colRow = table.querySelector("thead tr.price-table__head-row--cols");
      if (!colRow) {
        var theadRows = table.querySelectorAll("thead tr");
        if (!theadRows.length) return;
        colRow = theadRows[theadRows.length - 1];
      }
      var labels = [];
      colRow.querySelectorAll("th").forEach(function (th) {
        var text = (th.textContent || "").replace(/\s+/g, " ").trim();
        var colspan = parseInt(th.getAttribute("colspan") || "1", 10) || 1;
        for (var c = 0; c < colspan; c += 1) {
          labels.push(text);
        }
      });
      table.querySelectorAll("tbody tr").forEach(function (tr) {
        tr.querySelectorAll("td").forEach(function (td, idx) {
          if (td.classList.contains("price-table__service")) return;
          if (labels[idx]) {
            td.setAttribute("data-label", labels[idx]);
          }
        });
      });
    });
  })();

})();
