/**
 * Nyelvváltás — csak szöveg-fade, villanás nélkül.
 *
 * A „teljes oldalas” villanást a body opacity fade okozta (képek is megjelentek).
 * Most: képek/layout végig látszanak; csak a szöveg van elrejtve az első festéstől
 * (inline head CSS), majd egyetlen szöveg fade-in.
 */
(function () {
  var STORAGE_KEY = "langTextTransition";
  var SCROLL_KEY = "langScrollY";
  var EXIT_MS = 300;
  var ENTER_MS = 600;
  var navigating = false;
  var inputBlocked = false;
  var enterDone = false;

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function root() {
    return document.documentElement;
  }

  function clearPending() {
    var h = root();
    h.classList.remove("lang-enter-pending");
    h.classList.remove("lang-scroll-pending");
    h.classList.remove("lang-enter-ready");
    h.classList.remove("lang-exit");
    try {
      h.style.removeProperty("background-color");
      h.style.removeProperty("scroll-behavior");
      h.style.removeProperty("overflow");
      if (document.body) document.body.style.removeProperty("overflow");
    } catch (e) {}
  }

  function currentScrollY() {
    return window.scrollY || window.pageYOffset || root().scrollTop || 0;
  }

  function instantScrollTo(y) {
    try {
      root().style.scrollBehavior = "auto";
    } catch (e) {}
    try {
      window.scrollTo(0, y);
      root().scrollTop = y;
      if (document.body) document.body.scrollTop = y;
    } catch (e2) {}
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

  var TEXT_SEL = [
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "li",
    "label",
    "th",
    "td",
    "blockquote",
    "cite",
    ".hero__tagline",
    ".hero__title",
    ".hero__lead",
    ".section-title",
    ".section-subtitle",
    ".subpage-kicker",
    ".page-hero__title",
    ".page-hero__lead",
    ".stats__label",
    ".stats__value",
    ".stats__suffix",
    ".service-card__title",
    ".service-card__text",
    ".testimonial-card__quote",
    ".testimonial-card__name",
    ".faq-item__question",
    ".faq-item__answer",
    ".process-card__title",
    ".process-card__text",
    ".split-info__title",
    ".checklist__item span",
    ".service-panel__title",
    ".service-panel__panel-inner p",
    ".service-panel__panel-inner li",
    ".cta-banner__title",
    ".contact__title",
    ".contact__text",
    ".hazirend-rules__title",
    ".hazirend-rules__text",
    ".hazirend-hero-panel__title",
    ".hazirend-hero-panel__subtitle",
    ".hazirend-hero-panel__lead",
    ".kapcsolat-hero-panel__title",
    ".kapcsolat-hero-panel__lead",
    ".kapcsolat-hero-panel__line",
    ".price-table__service",
    ".price-table__price",
    ".form__status",
    ".btn",
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
  }

  function runEnter() {
    var y = readScroll();
    if (y >= 0) {
      root().classList.add("lang-scroll-pending");
      instantScrollTo(y);
    }

    var flag = false;
    try {
      flag = sessionStorage.getItem(STORAGE_KEY) === "1";
    } catch (e) {}

    if (prefersReducedMotion() || !flag) {
      clearPending();
      clearScrollStorage();
      try {
        sessionStorage.removeItem(STORAGE_KEY);
      } catch (e) {}
      return;
    }

    var main = document.querySelector("main");
    if (!main) {
      clearPending();
      clearScrollStorage();
      try {
        sessionStorage.removeItem(STORAGE_KEY);
      } catch (e) {}
      return;
    }

    /* Szöveg maradjon 0-n (pending + enter), képek látszanak — nincs body-flash */
    inputBlocked = true;
    main.classList.add("lang-text-motion", "lang-text-motion--enter");
    var nodes = mark(main);
    if (y >= 0) instantScrollTo(y);

    try {
      sessionStorage.removeItem(STORAGE_KEY);
    } catch (e) {}
    clearScrollStorage();

    requestAnimationFrame(function () {
      if (y >= 0) instantScrollTo(y);
      requestAnimationFrame(function () {
        if (y >= 0) instantScrollTo(y);

        /* Előbb enter-active (szöveg 0→1 transition), pending csak utána le — nincs snap */
        main.classList.add("lang-text-motion--enter-active");
        try {
          void main.offsetHeight;
        } catch (e) {}

        root().classList.remove("lang-enter-pending");
        root().classList.remove("lang-scroll-pending");
        try {
          root().style.removeProperty("background-color");
          root().style.removeProperty("scroll-behavior");
        } catch (e2) {}
        inputBlocked = false;
      });
    });

    window.setTimeout(function () {
      finishEnter(main, nodes);
    }, ENTER_MS);

    window.setTimeout(function () {
      finishEnter(main, nodes);
    }, 1600);
  }

  function navigateTo(href) {
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
        if (!a || a.classList.contains("lang-switch__link--current")) return;
        if (e.defaultPrevented || e.button !== 0) return;
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

        var hrefAttr = a.getAttribute("href");
        if (!hrefAttr || hrefAttr.charAt(0) === "#") return;

        if (navigating) {
          e.preventDefault();
          return;
        }

        saveScroll();
        if (prefersReducedMotion()) return;

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
          root().style.overflow = "hidden";
          if (document.body) document.body.style.overflow = "hidden";
        } catch (err2) {}
        inputBlocked = true;

        mark(main);
        main.classList.add("lang-text-motion", "lang-text-motion--exit");

        var target = a.href;
        window.setTimeout(function () {
          navigateTo(target);
        }, EXIT_MS);

        window.setTimeout(function () {
          if (document.visibilityState !== "hidden") navigateTo(target);
        }, EXIT_MS + 700);
      },
      true
    );
  }

  try {
    if (sessionStorage.getItem(SCROLL_KEY) != null && "scrollRestoration" in history) {
      history.scrollRestoration = "manual";
    }
  } catch (e) {}

  if (typeof window.__langScrollY === "number") {
    instantScrollTo(window.__langScrollY);
  }

  window.addEventListener("pageshow", function (ev) {
    if (ev.persisted) {
      clearPending();
      inputBlocked = false;
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

  window.setTimeout(function () {
    if (root().classList.contains("lang-enter-pending")) {
      var main = document.querySelector("main");
      var nodes = main ? mark(main) : null;
      if (main) {
        main.classList.add("lang-text-motion", "lang-text-motion--enter", "lang-text-motion--enter-active");
      }
      clearPending();
      inputBlocked = false;
      window.setTimeout(function () {
        finishEnter(main, nodes);
      }, 50);
    }
  }, 2000);
})();
