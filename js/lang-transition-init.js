/**
 * Nyelvváltáskor csak a <main> szöveges tartalma animálódik (finom fade, enyhe elmozdulás, blur nélkül).
 * A <head>-ben lévő szinkron script (lang-enter-pending) megakadályozza az első festésnél a szöveg villanását.
 */
(function () {
  var STORAGE_KEY = "langTextTransition";
  var EXIT_MS = 480;
  var ENTER_TOTAL_MS = 720;

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function clearLangPendingSurface() {
    document.documentElement.classList.remove("lang-enter-pending");
    try {
      document.documentElement.style.removeProperty("background-color");
    } catch (e) {}
  }

  function textTargets(main) {
    return main.querySelectorAll(
      [
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
        ".kapcsolat-hero-panel__line",
        ".price-table__service",
        ".price-table__price",
        ".form__status",
        ".btn",
      ].join(",")
    );
  }

  function runEnter() {
    var flag = false;
    try {
      flag = sessionStorage.getItem(STORAGE_KEY) === "1";
    } catch (e) {}

    if (prefersReducedMotion()) {
      clearLangPendingSurface();
      try {
        sessionStorage.removeItem(STORAGE_KEY);
      } catch (e) {}
      return;
    }

    if (!flag) {
      clearLangPendingSurface();
      return;
    }

    var main = document.querySelector("main");
    if (!main) {
      clearLangPendingSurface();
      try {
        sessionStorage.removeItem(STORAGE_KEY);
      } catch (e) {}
      return;
    }

    main.classList.add("lang-text-motion", "lang-text-motion--enter");
    var nodes = textTargets(main);
    for (var i = 0; i < nodes.length; i++) {
      nodes[i].classList.add("lang-text-motion__el");
    }

    clearLangPendingSurface();

    try {
      sessionStorage.removeItem(STORAGE_KEY);
    } catch (e) {}

    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        main.classList.add("lang-text-motion--enter-active");
      });
    });

    window.setTimeout(function () {
      main.classList.remove(
        "lang-text-motion",
        "lang-text-motion--enter",
        "lang-text-motion--enter-active"
      );
      for (var j = 0; j < nodes.length; j++) {
        nodes[j].classList.remove("lang-text-motion__el");
      }
    }, ENTER_TOTAL_MS);
  }

  function bindExit() {
    if (prefersReducedMotion()) return;

    document.addEventListener(
      "click",
      function (e) {
        var a = e.target.closest && e.target.closest("a.lang-switch__link");
        if (!a || a.classList.contains("lang-switch__link--current")) return;
        if (e.defaultPrevented) return;
        if (e.button !== 0) return;
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

        var href = a.getAttribute("href");
        if (!href || href.charAt(0) === "#") return;

        var main = document.querySelector("main");
        if (!main) return;

        e.preventDefault();

        try {
          sessionStorage.setItem(STORAGE_KEY, "1");
        } catch (err) {}

        var nodes = textTargets(main);
        for (var i = 0; i < nodes.length; i++) {
          nodes[i].classList.add("lang-text-motion__el");
        }
        main.classList.add("lang-text-motion", "lang-text-motion--exit");

        window.setTimeout(function () {
          window.location.href = a.href;
        }, EXIT_MS);
      },
      true
    );
  }

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
