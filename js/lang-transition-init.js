/**
 * Nyelvváltás — fade-out/fade-in + mid-scroll villanásmentes restore.
 *
 * Folyamat:
 *  1) Kilépés: scroll mentése, main/szöveg fade-out, navigáció
 *  2) Belépés (inline head + ez a fájl): scroll vissza, majd fade-in
 *  3) Mid-scroll: body visibility:hidden + header látható, amíg a scroll helyreáll
 */
(function () {
  if (window.__langTransitionBound) return;
  window.__langTransitionBound = true;

  var STORAGE_KEY = "langTextTransition";
  var SCROLL_KEY = "langScrollY";
  var EXIT_MS = 280;
  var ENTER_MS = 520;
  var navigating = false;
  var inputBlocked = false;
  var enterDone = false;
  var enterTimer = null;
  var safetyTimer = null;
  var navTimer = null;
  var navFallbackTimer = null;

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function root() {
    return document.documentElement;
  }

  function clearInlineFade(el) {
    if (!el) return;
    try {
      el.style.removeProperty("opacity");
      el.style.removeProperty("transition");
    } catch (e) {}
  }

  function clearPending() {
    var h = root();
    h.classList.remove(
      "lang-enter-pending",
      "lang-scroll-pending",
      "lang-content-pending",
      "lang-exit"
    );
    try {
      h.style.removeProperty("background-color");
      h.style.removeProperty("scroll-behavior");
    } catch (e) {}
    clearInlineFade(document.querySelector("main"));
    clearInlineFade(document.querySelector(".site-footer"));
  }

  function currentScrollY() {
    return window.scrollY || window.pageYOffset || root().scrollTop || 0;
  }

  function instantScrollTo(y) {
    var h = root();
    try {
      h.style.scrollBehavior = "auto";
    } catch (e) {}
    try {
      if (typeof window.scrollTo === "function") {
        try {
          window.scrollTo({ top: y, left: 0, behavior: "instant" });
        } catch (e1) {
          try {
            window.scrollTo({ top: y, left: 0, behavior: "auto" });
          } catch (e2) {
            window.scrollTo(0, y);
          }
        }
      }
      h.scrollTop = y;
      if (document.body) document.body.scrollTop = y;
    } catch (e3) {}
  }

  function docScrollHeight() {
    var b = document.body;
    var h = root();
    return Math.max(
      b ? b.scrollHeight : 0,
      b ? b.offsetHeight : 0,
      h.scrollHeight,
      h.offsetHeight,
      h.clientHeight
    );
  }

  function saveScroll() {
    try {
      sessionStorage.setItem(SCROLL_KEY, String(Math.round(currentScrollY())));
      if ("scrollRestoration" in history) history.scrollRestoration = "manual";
    } catch (e) {}
  }

  function readScroll() {
    if (typeof window.__langScrollY === "number" && window.__langScrollY >= 0) {
      return window.__langScrollY;
    }
    try {
      var raw = sessionStorage.getItem(SCROLL_KEY);
      if (raw == null) return -1;
      var y = parseInt(raw, 10);
      return isNaN(y) || y < 0 ? -1 : y;
    } catch (e) {
      return -1;
    }
  }

  function clearScrollStorage() {
    try {
      sessionStorage.removeItem(SCROLL_KEY);
    } catch (e) {}
    try {
      delete window.__langScrollY;
    } catch (e2) {
      window.__langScrollY = undefined;
    }
  }

  function blockInput(e) {
    if (!inputBlocked) return;
    e.preventDefault();
  }

  document.addEventListener("wheel", blockInput, { capture: true, passive: false });
  document.addEventListener("touchmove", blockInput, { capture: true, passive: false });
  document.addEventListener(
    "keydown",
    function (e) {
      if (!inputBlocked) return;
      var k = e.key;
      if (k === "ArrowUp" || k === "ArrowDown" || k === "PageUp" || k === "PageDown" || k === " " || k === "Home" || k === "End") {
        e.preventDefault();
      }
    },
    { capture: true }
  );

  var TEXT_SEL = [
    "h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "label", "th", "td",
    "blockquote", "cite",
    ".hero__tagline", ".hero__title", ".hero__lead",
    ".section-title", ".section-subtitle", ".subpage-kicker",
    ".page-hero__title", ".page-hero__lead",
    ".stats__label", ".stats__value", ".stats__suffix",
    ".service-card__title", ".service-card__text",
    ".testimonial-card__quote", ".testimonial-card__name",
    ".faq-item__question", ".faq-item__answer",
    ".process-card__title", ".process-card__text",
    ".split-info__title", ".checklist__item span",
    ".service-panel__title", ".service-panel__panel-inner p", ".service-panel__panel-inner li",
    ".cta-banner__title", ".contact__title", ".contact__text",
    ".hazirend-rules__title", ".hazirend-rules__text",
    ".hazirend-hero-panel__title", ".hazirend-hero-panel__subtitle", ".hazirend-hero-panel__lead",
    ".kapcsolat-hero-panel__title", ".kapcsolat-hero-panel__lead", ".kapcsolat-hero-panel__line",
    ".price-table__service", ".price-table__price", ".form__status", ".btn",
  ].join(",");

  function textTargets(main) {
    return main.querySelectorAll(TEXT_SEL);
  }

  function mark(main) {
    var nodes = textTargets(main);
    for (var i = 0; i < nodes.length; i++) {
      nodes[i].classList.add("lang-text-motion__el");
    }
    return nodes;
  }

  function unmark(nodes) {
    if (!nodes) return;
    for (var i = 0; i < nodes.length; i++) {
      nodes[i].classList.remove("lang-text-motion__el");
    }
  }

  function finishEnter(main, nodes) {
    if (enterDone) return;
    enterDone = true;
    if (enterTimer) {
      clearTimeout(enterTimer);
      enterTimer = null;
    }
    if (safetyTimer) {
      clearTimeout(safetyTimer);
      safetyTimer = null;
    }
    if (main) {
      main.classList.remove(
        "lang-text-motion",
        "lang-text-motion--enter",
        "lang-text-motion--enter-active",
        "lang-text-motion--exit"
      );
    }
    unmark(nodes);
    clearPending();
    inputBlocked = false;
    navigating = false;
  }

  function restoreScrollThen(y, done) {
    if (y <= 0) {
      instantScrollTo(0);
      done();
      return;
    }

    root().classList.add("lang-scroll-pending");
    root().classList.add("lang-content-pending");
    try {
      root().style.scrollBehavior = "auto";
    } catch (e) {}

    var attempts = 0;
    var maxAttempts = 60;

    function tick() {
      attempts += 1;
      instantScrollTo(y);

      var maxY = Math.max(0, docScrollHeight() - window.innerHeight);
      var target = Math.min(y, maxY);
      var pos = currentScrollY();
      var closeEnough = Math.abs(pos - target) <= 2;
      var tallEnough = docScrollHeight() >= Math.min(y + window.innerHeight * 0.35, y + 120);

      if ((closeEnough && tallEnough) || attempts >= maxAttempts) {
        instantScrollTo(target);
        requestAnimationFrame(function () {
          instantScrollTo(target);
          requestAnimationFrame(function () {
            instantScrollTo(target);
            done();
          });
        });
        return;
      }
      requestAnimationFrame(tick);
    }

    requestAnimationFrame(tick);
  }

  function startTextEnter(main, nodes, y) {
    if (y > 0) instantScrollTo(y);

    main.classList.add("lang-text-motion--enter-active");
    try {
      void main.offsetHeight;
    } catch (e) {}

    var footer = document.querySelector(".site-footer");

    /*
     * 1) visibility maszk le (body látszik), de main még opacity 0
     * 2) scroll újra
     * 3) main + footer + szöveg együtt fade-in
     */
    root().classList.remove("lang-scroll-pending");
    if (y > 0) instantScrollTo(y);

    requestAnimationFrame(function () {
      if (y > 0) instantScrollTo(y);

      root().classList.remove("lang-enter-pending");
      root().classList.remove("lang-content-pending");
      try {
        root().style.removeProperty("background-color");
      } catch (e2) {}

      if (y > 0) {
        main.style.transition = "opacity 0.45s cubic-bezier(0.22, 0.61, 0.36, 1)";
        main.style.opacity = "1";
        if (footer) {
          footer.style.transition = "opacity 0.45s cubic-bezier(0.22, 0.61, 0.36, 1)";
          footer.style.opacity = "1";
        }
        instantScrollTo(y);
      }

      inputBlocked = false;
      enterTimer = window.setTimeout(function () {
        finishEnter(main, nodes);
      }, ENTER_MS);
    });
  }

  function abandonEnter() {
    clearPending();
    clearScrollStorage();
    try {
      sessionStorage.removeItem(STORAGE_KEY);
    } catch (e) {}
    inputBlocked = false;
    navigating = false;
  }

  function runEnter() {
    var y = readScroll();

    var flag = false;
    try {
      flag = sessionStorage.getItem(STORAGE_KEY) === "1";
    } catch (e) {}

    if (prefersReducedMotion() || !flag) {
      if (y > 0) instantScrollTo(y);
      clearPending();
      clearScrollStorage();
      try {
        sessionStorage.removeItem(STORAGE_KEY);
      } catch (e) {}
      return;
    }

    var main = document.querySelector("main");
    if (!main) {
      abandonEnter();
      return;
    }

    enterDone = false;
    inputBlocked = true;
    try {
      root().style.scrollBehavior = "auto";
    } catch (e) {}

    /* Mid-scroll: main/footer tartsuk opacity 0-n a CSS mellett is */
    if (y > 0) {
      root().classList.add("lang-scroll-pending");
      root().classList.add("lang-content-pending");
      main.style.opacity = "0";
      var footer = document.querySelector(".site-footer");
      if (footer) footer.style.opacity = "0";
    }

    main.classList.add("lang-text-motion", "lang-text-motion--enter");
    var nodes = mark(main);

    try {
      sessionStorage.removeItem(STORAGE_KEY);
    } catch (e) {}

    safetyTimer = window.setTimeout(function () {
      if (y > 0) instantScrollTo(y);
      if (!main.classList.contains("lang-text-motion--enter-active")) {
        main.classList.add("lang-text-motion--enter-active");
      }
      finishEnter(main, nodes);
    }, 2800);

    restoreScrollThen(Math.max(0, y), function () {
      clearScrollStorage();
      startTextEnter(main, nodes, Math.max(0, y));
    });
  }

  function navigateTo(href) {
    if (navTimer) {
      clearTimeout(navTimer);
      navTimer = null;
    }
    if (navFallbackTimer) {
      clearTimeout(navFallbackTimer);
      navFallbackTimer = null;
    }
    try {
      window.location.assign(href);
    } catch (e) {
      window.location.href = href;
    }
  }

  function bindExit() {
    document.addEventListener(
      "click",
      function (e) {
        var a = e.target.closest && e.target.closest("a.lang-switch__link");
        if (!a) return;

        /* Aktuális nyelv: soha ne töltse újra az oldalt */
        if (a.classList.contains("lang-switch__link--current") || a.getAttribute("aria-current") === "true") {
          e.preventDefault();
          return;
        }

        if (e.defaultPrevented || e.button !== 0) return;
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

        var hrefAttr = a.getAttribute("href");
        if (!hrefAttr || hrefAttr.charAt(0) === "#") return;

        if (navigating) {
          e.preventDefault();
          return;
        }

        saveScroll();

        if (prefersReducedMotion()) {
          /* Scroll mentve — a böngésző követheti a linket */
          return;
        }

        var main = document.querySelector("main");
        if (!main) return;

        e.preventDefault();
        navigating = true;

        try {
          sessionStorage.setItem(STORAGE_KEY, "1");
        } catch (err) {}

        root().classList.add("lang-exit");
        try {
          root().style.scrollBehavior = "auto";
        } catch (err2) {}
        inputBlocked = true;

        var y = currentScrollY();
        mark(main);
        main.classList.add("lang-text-motion", "lang-text-motion--exit");

        /* Mid-scroll: képek se villanhassanak — main is fade-out */
        if (y > 0) {
          main.style.transition = "opacity 0.26s cubic-bezier(0.22, 0.61, 0.36, 1)";
          main.style.opacity = "0";
          var footer = document.querySelector(".site-footer");
          if (footer) {
            footer.style.transition = "opacity 0.26s cubic-bezier(0.22, 0.61, 0.36, 1)";
            footer.style.opacity = "0";
          }
        }

        var target = a.href;
        navTimer = window.setTimeout(function () {
          navigateTo(target);
        }, EXIT_MS);

        navFallbackTimer = window.setTimeout(function () {
          if (document.visibilityState !== "hidden") navigateTo(target);
        }, EXIT_MS + 900);
      },
      true
    );
  }

  function hardResetFromCache() {
    clearPending();
    inputBlocked = false;
    navigating = false;
    enterDone = true;
    if (enterTimer) clearTimeout(enterTimer);
    if (safetyTimer) clearTimeout(safetyTimer);
    if (navTimer) clearTimeout(navTimer);
    if (navFallbackTimer) clearTimeout(navFallbackTimer);
    enterTimer = safetyTimer = navTimer = navFallbackTimer = null;
    var main = document.querySelector("main");
    if (main) {
      main.classList.remove(
        "lang-text-motion",
        "lang-text-motion--enter",
        "lang-text-motion--enter-active",
        "lang-text-motion--exit"
      );
    }
    unmark(document.querySelectorAll(".lang-text-motion__el"));
  }

  try {
    if (sessionStorage.getItem(SCROLL_KEY) != null && "scrollRestoration" in history) {
      history.scrollRestoration = "manual";
    }
  } catch (e) {}

  if (typeof window.__langScrollY === "number" && window.__langScrollY > 0) {
    instantScrollTo(window.__langScrollY);
  }

  window.addEventListener("pageshow", function (ev) {
    if (ev.persisted) {
      hardResetFromCache();
    }
  });

  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "visible" && navigating && !document.querySelector("html.lang-exit")) {
      /* Navigáció megszakadt / bfcache-szerű visszatérés */
      hardResetFromCache();
    }
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      runEnter();
      bindExit();
    });
  } else {
    runEnter();
    bindExit();
  }
})();
