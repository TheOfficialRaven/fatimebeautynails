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
    var media = modal.querySelector(".ref-lightbox__media");
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

    var swipeTarget = media || figure;
    if (swipeTarget) {
      swipeTarget.addEventListener(
        "touchstart",
        function (e) {
          touchStartX = e.changedTouches[0].screenX;
        },
        { passive: true }
      );
      swipeTarget.addEventListener(
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

  /* Testimonials karousel: mobil = 1 kártya / dia; asztal = 2 kártya / „oldal”. Viewport magasság = aktív dia. */
  (function testimonialsCarousel() {
    var root = document.querySelector("[data-testimonials-carousel]");
    if (!root) return;

    var viewport = root.querySelector(".testimonials-carousel__viewport");
    var track = root.querySelector(".testimonials-carousel__track");
    var slides = root.querySelectorAll(".testimonials-carousel__slide");
    var dotsMobile = root.querySelectorAll(".testimonials-carousel__dots--mobile .testimonials-carousel__dot");
    var dotsDesktop = root.querySelectorAll(".testimonials-carousel__dots--desktop .testimonials-carousel__dot");
    var prevBtns = root.querySelectorAll("[data-testimonials-prev]");
    var nextBtns = root.querySelectorAll("[data-testimonials-next]");
    var n = slides.length;
    var slideIdx = 0;
    var pageIdx = 0;
    var timer = null;
    var intervalMs = 15000;
    var lastMobile = null;
    var resizeT;

    if (!track || !viewport || n < 1) return;

    function isMobile() {
      return window.matchMedia("(max-width: 1024px)").matches;
    }

    function parseGapPx() {
      var cs = window.getComputedStyle(track);
      var g = cs.gap || cs.columnGap || "0";
      var parsed = parseFloat(g);
      return isNaN(parsed) ? 0 : parsed;
    }

    function updateViewportHeight() {
      /* Két rAF: stabil layout; ne állítsuk height: auto-ra — az megszakítaná a CSS height átmenetet. */
      window.requestAnimationFrame(function () {
        window.requestAnimationFrame(function () {
          var h = 0;
          if (isMobile()) {
            slides.forEach(function (slide) {
              h = Math.max(h, slide.offsetHeight);
            });
          } else {
            for (var i = 0; i < n; i += 2) {
              var a = slides[i];
              var b = slides[i + 1];
              h = Math.max(h, Math.max(a ? a.offsetHeight : 0, b ? b.offsetHeight : 0));
            }
          }
          if (h > 0) viewport.style.height = Math.round(h) + "px";
        });
      });
    }

    function syncDesktopPairHeights(mobile) {
      slides.forEach(function (slide) {
        slide.style.height = "";
      });
      if (mobile) return;

      for (var i = 0; i < n; i += 2) {
        var a = slides[i];
        var b = slides[i + 1];
        if (!a) continue;
        var ah = a.offsetHeight;
        var bh = b ? b.offsetHeight : 0;
        var h = Math.max(ah, bh);
        if (h > 0) {
          a.style.height = h + "px";
          if (b) b.style.height = h + "px";
        }
      }
    }

    function measure() {
      var vw = Math.round(viewport.getBoundingClientRect().width);
      if (vw < 1) return;
      var gapPx = parseGapPx();
      var mobile = isMobile();
      var slideW;
      if (mobile) {
        slideW = vw;
        slides.forEach(function (slide) {
          slide.style.flex = "0 0 " + slideW + "px";
          slide.style.width = slideW + "px";
          slide.style.maxWidth = slideW + "px";
          slide.style.minWidth = slideW + "px";
        });
        track.style.transform = "translateX(-" + Math.round(slideIdx * (slideW + gapPx)) + "px)";
      } else {
        slideW = Math.round((vw - gapPx) / 2);
        slides.forEach(function (slide) {
          slide.style.flex = "0 0 " + slideW + "px";
          slide.style.width = slideW + "px";
          slide.style.maxWidth = slideW + "px";
          slide.style.minWidth = slideW + "px";
        });
        track.style.transform = "translateX(-" + Math.round(pageIdx * (vw + gapPx)) + "px)";
      }
      syncDesktopPairHeights(mobile);
      updateViewportHeight();
    }

    function setAria() {
      var mobile = isMobile();
      slides.forEach(function (slide, idx) {
        var visible = false;
        if (mobile) visible = idx === slideIdx;
        else visible = idx === pageIdx * 2 || idx === pageIdx * 2 + 1;
        slide.setAttribute("aria-hidden", visible ? "false" : "true");
      });
      dotsMobile.forEach(function (dot, idx) {
        var on = mobile && idx === slideIdx;
        dot.classList.toggle("is-active", on);
        dot.setAttribute("aria-selected", on ? "true" : "false");
        dot.tabIndex = on ? 0 : -1;
      });
      dotsDesktop.forEach(function (dot, idx) {
        var on = !mobile && idx === pageIdx;
        dot.classList.toggle("is-active", on);
        dot.setAttribute("aria-selected", on ? "true" : "false");
        dot.tabIndex = on ? 0 : -1;
      });
    }

    function goSlide(to) {
      slideIdx = ((to % n) + n) % n;
      measure();
      setAria();
    }

    function goPage(to) {
      var maxPage = Math.max(0, Math.ceil(n / 2) - 1);
      pageIdx = ((to % (maxPage + 1)) + (maxPage + 1)) % (maxPage + 1);
      measure();
      setAria();
    }

    function next() {
      if (isMobile()) goSlide(slideIdx + 1);
      else goPage(pageIdx + 1);
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

    function syncModeIfChanged() {
      var mobile = isMobile();
      if (lastMobile === null) {
        lastMobile = mobile;
        return;
      }
      if (mobile !== lastMobile) {
        if (mobile) slideIdx = pageIdx * 2;
        else pageIdx = Math.min(Math.max(0, Math.ceil(n / 2) - 1), Math.floor(slideIdx / 2));
        lastMobile = mobile;
      }
    }

    dotsMobile.forEach(function (dot, idx) {
      dot.addEventListener("click", function () {
        goSlide(idx);
        stopAutoplay();
        startAutoplay();
      });
    });

    dotsDesktop.forEach(function (dot, idx) {
      dot.addEventListener("click", function () {
        goPage(idx);
        stopAutoplay();
        startAutoplay();
      });
    });

    prevBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (isMobile()) goSlide(slideIdx - 1);
        else goPage(pageIdx - 1);
        stopAutoplay();
        startAutoplay();
      });
    });

    nextBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (isMobile()) goSlide(slideIdx + 1);
        else goPage(pageIdx + 1);
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

    window.addEventListener("resize", function () {
      syncModeIfChanged();
      clearTimeout(resizeT);
      resizeT = setTimeout(function () {
        measure();
      }, 80);
    });

    var mqBr = window.matchMedia("(max-width: 1024px)");
    function onMqChange() {
      syncModeIfChanged();
      measure();
      setAria();
    }
    if (mqBr.addEventListener) mqBr.addEventListener("change", onMqChange);
    else if (mqBr.addListener) mqBr.addListener(onMqChange);

    slides.forEach(function (slide) {
      Array.prototype.forEach.call(slide.querySelectorAll("img"), function (img) {
        img.addEventListener("load", function () {
          updateViewportHeight();
        });
      });
    });

    lastMobile = isMobile();
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

  (function welcomeCouponPopup() {
    var delayMs = 10000;
    var popupRoot = null;
    var onEsc = null;

    function isHuLanguage() {
      var lang = ((document.documentElement && document.documentElement.lang) || "").toLowerCase();
      return lang.indexOf("hu") === 0;
    }

    function getPopupImagePath() {
      var path = window.location.pathname || "";
      var isHuPage = /(^|\/)hu(\/|$)/i.test(path);
      return isHuPage ? "../assets/imgs/popup_img.png" : "assets/imgs/popup_img.png";
    }

    function getPopupCopy() {
      if (isHuLanguage()) {
        return {
          closeLabel: "Bezárás",
          imageAlt: "Kedvezményes ajánlat",
          title: "10% KEDVEZMÉNY!",
          text:
            "Először jársz a szalonban? Minden első vendégem részére egy 10%-os kupont biztosítom, amit az e-mail címedre küldjük ki. Töltsd ki az alábbi mezőket és élj a lehetőséggel.",
          namePlaceholder: "Teljes név",
          emailPlaceholder: "E-mail cím",
          privacyText: "Elolvastam és elfogadom az",
          privacyLinkText: "adatkezelési tájékoztatót.",
          privacyHref: "hazirend.html",
          submitLabel: "Kérem a kupont!",
        };
      }
      return {
        closeLabel: "Schliessen",
        imageAlt: "Rabattangebot",
        title: "10% RABATT!",
        text:
          "Bist du zum ersten Mal im Salon? Fur alle Neukundinnen gibt es einen 10%-Gutschein, den ich dir per E-Mail zusende. Fulle bitte die Felder unten aus und sichere dir dein Angebot.",
        namePlaceholder: "Vollstandiger Name",
        emailPlaceholder: "E-Mail-Adresse",
        privacyText: "Ich habe die",
        privacyLinkText: "Datenschutzerklarung gelesen und akzeptiere sie.",
        privacyHref: "hausordnung.html",
        submitLabel: "Gutschein anfordern",
      };
    }

    function closePopup() {
      if (!popupRoot) return;
      popupRoot.classList.remove("coupon-popup--visible");
      popupRoot.setAttribute("aria-hidden", "true");
      if (onEsc) {
        document.removeEventListener("keydown", onEsc);
        onEsc = null;
      }
      window.setTimeout(function () {
        if (popupRoot && popupRoot.parentNode) {
          popupRoot.parentNode.removeChild(popupRoot);
        }
        popupRoot = null;
      }, 920);
    }

    function buildPopup() {
      var imgSrc = getPopupImagePath();
      var copy = getPopupCopy();
      var wrapper = document.createElement("div");
      wrapper.className = "coupon-popup";
      wrapper.setAttribute("aria-hidden", "true");
      wrapper.innerHTML =
        '<div class="coupon-popup__backdrop" data-popup-close="true"></div>' +
        '<section class="coupon-popup__panel" role="dialog" aria-modal="true" aria-labelledby="coupon-popup-title">' +
        '<button class="coupon-popup__close" type="button" aria-label="' +
        copy.closeLabel +
        '" data-popup-close="true">&times;</button>' +
        '<img class="coupon-popup__image" src="' +
        imgSrc +
        '" alt="' +
        copy.imageAlt +
        '" loading="eager" decoding="async" />' +
        '<div class="coupon-popup__content">' +
        '<h2 class="coupon-popup__title" id="coupon-popup-title">' +
        copy.title +
        "</h2>" +
        '<p class="coupon-popup__text">' +
        copy.text +
        "</p>" +
        '<form class="coupon-popup__form" action="#" method="post" novalidate>' +
        '<input class="coupon-popup__input" type="text" name="name" autocomplete="name" placeholder="' +
        copy.namePlaceholder +
        '" />' +
        '<input class="coupon-popup__input" type="email" name="email" autocomplete="email" placeholder="' +
        copy.emailPlaceholder +
        '" />' +
        '<label class="coupon-popup__check">' +
        '<input class="coupon-popup__check-input" type="checkbox" name="privacy" />' +
        "<span>" +
        copy.privacyText +
        ' <a href="' +
        copy.privacyHref +
        '">' +
        copy.privacyLinkText +
        "</a></span>" +
        "</label>" +
        '<button class="coupon-popup__submit" type="submit">' +
        copy.submitLabel +
        "</button>" +
        "</form>" +
        "</div>" +
        "</section>";

      wrapper.addEventListener("click", function (e) {
        var closeTarget = e.target.closest("[data-popup-close='true']");
        if (closeTarget) closePopup();
      });

      onEsc = function (e) {
        if (e.key === "Escape") closePopup();
      };
      document.addEventListener("keydown", onEsc);

      popupRoot = wrapper;
      document.body.appendChild(popupRoot);

      /* Force one full paint cycle before toggling visible state,
         otherwise some browsers skip the enter transition. */
      void popupRoot.offsetWidth;
      window.requestAnimationFrame(function () {
        if (!popupRoot) return;
        window.requestAnimationFrame(function () {
          if (!popupRoot) return;
          popupRoot.classList.add("coupon-popup--visible");
          popupRoot.setAttribute("aria-hidden", "false");
        });
      });
    }

    function initPopup() {
      window.setTimeout(buildPopup, delayMs);
    }

    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", initPopup, { once: true });
    } else {
      initPopup();
    }
  })();

})();


