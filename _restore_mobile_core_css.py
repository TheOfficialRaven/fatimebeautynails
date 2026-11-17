# -*- coding: utf-8 -*-
"""Move site-wide mobile (≤900) rules from pages CSS back into core styles.css.

Homepage does not load styles-pages — without these rules mobile nav/sections break
when deferred core CSS overrides critical CSS.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORE = ROOT / "css" / "styles.css"
PAGES = ROOT / "css" / "styles-pages.css"

MARKER = "/* MOBILE_CORE_SHARED: nav + home sections (must be in core) */"

SHARED_MOBILE = r'''
  /* MOBILE_CORE_SHARED: nav + home sections (must be in core) */

  .testimonial-card__quote {
    font-size: 0.875rem;
    font-weight: 300;
    line-height: 1.3;
  }

  .why-me {
    min-height: auto;
    overflow-x: hidden;
  }

  .why-me__grid {
    min-height: auto;
    grid-template-columns: 1fr;
  }

  .why-me__media {
    order: -1;
    width: 100vw;
    min-width: 100vw;
    max-width: none;
    margin-left: calc(50% - 50vw);
    position: relative;
    min-height: min(52vh, 480px);
    max-height: 65vh;
    aspect-ratio: 4 / 5;
    justify-self: stretch;
    overflow: hidden;
  }

  .why-me__content {
    padding: var(--section-space) clamp(1.5rem, 5vw, 2rem);
    align-items: center;
    text-align: center;
  }

  .why-me__content .stats,
  .why-me__content .stats.stats--why {
    justify-items: center;
    text-align: center;
  }

  .why-me__content .btn--why-cta {
    align-self: center;
  }

  .contact {
    --contact-panel-min-h: 0;
    height: auto;
    max-height: none;
    min-height: auto;
    overflow: visible;
  }

  .contact__split {
    flex-direction: column;
    height: auto;
    max-height: none;
    min-height: auto;
    overflow: visible;
  }

  .contact.contact--after-overlap-hero .contact__split {
    height: auto;
    max-height: none;
    min-height: auto;
    overflow: visible;
  }

  .contact__media {
    flex: none;
    max-width: none;
    width: 100%;
    position: relative;
    top: auto;
    align-self: stretch;
    height: auto;
    max-height: none;
    min-height: min(42vh, 420px);
    aspect-ratio: 4 / 3;
  }

  .contact__form-wrap {
    flex: none;
    max-width: none;
    width: 100%;
    height: auto;
    max-height: none;
    min-height: 0;
    overflow: visible;
    padding: clamp(1.35rem, 4vw, 2rem) clamp(1.25rem, 5vw, 2rem);
  }

  .footer__grid {
    grid-template-columns: 1fr;
    gap: 2.25rem;
  }

  .nav-toggle {
    display: flex;
  }

  .nav {
    position: fixed;
    inset: var(--header-h) 0 auto 0;
    background: var(--color-white);
    flex-direction: column;
    align-items: stretch;
    padding: 1.5rem 24px 2rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
    box-shadow: 0 14px 34px rgba(43, 74, 66, 0.08);
    transform-origin: top center;
    transform: translateY(-10px);
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    /* Zárt állapot: nincs transition — breakpoint váltáskor ne villanjon fel */
    transition: none;
  }

  .site-header.is-open .nav {
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
    transition:
      transform 0.58s cubic-bezier(0.22, 1, 0.36, 1),
      opacity 0.5s ease,
      visibility 0s;
  }

  /* Bezárás animáció csak manuális záráskor */
  .site-header.is-nav-closing .nav {
    transition:
      transform 0.52s cubic-bezier(0.4, 0, 0.2, 1),
      opacity 0.42s ease,
      visibility 0s linear 0.52s;
  }

  .site-header.nav-mq-lock .nav,
  .site-header.nav-mq-lock .nav__list > .nav__item,
  .site-header.nav-mq-lock .nav .btn--header-cta,
  .site-header.nav-mq-lock .lang-switch {
    transition: none !important;
  }

  .nav__list {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .nav__list > .nav__item,
  .nav .btn--header-cta,
  .lang-switch {
    opacity: 0;
    transform: translateY(-8px);
    transition:
      opacity 0.42s ease,
      transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
  }

  .site-header.is-open .nav__list > .nav__item,
  .site-header.is-open .nav .btn--header-cta,
  .site-header.is-open .lang-switch {
    opacity: 1;
    transform: translateY(0);
  }

  .site-header.is-open .nav__list > .nav__item:nth-child(1) { transition-delay: 0.08s; }
  .site-header.is-open .nav__list > .nav__item:nth-child(2) { transition-delay: 0.14s; }
  .site-header.is-open .nav__list > .nav__item:nth-child(3) { transition-delay: 0.2s; }
  .site-header.is-open .nav__list > .nav__item:nth-child(4) { transition-delay: 0.26s; }
  .site-header.is-open .nav__list > .nav__item:nth-child(5) { transition-delay: 0.32s; }
  .site-header.is-open .nav .btn--header-cta { transition-delay: 0.38s; }
  .site-header.is-open .lang-switch { transition-delay: 0.44s; }

  .nav .btn--header-cta {
    margin-top: 0.5rem;
    width: 100%;
    align-self: stretch;
    text-align: center;
  }

  .lang-switch {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--color-border);
    width: 100%;
    justify-content: flex-start;
    margin-left: 0;
  }

  .nav__sub {
    display: block;
    position: static;
    left: auto;
    top: auto;
    margin: 0.35rem 0 0.15rem 0.5rem;
    padding: 0;
    min-width: 0;
    border: none;
    box-shadow: none;
    background: transparent;
    max-height: 0;
    opacity: 0;
    visibility: hidden;
    overflow: hidden;
    pointer-events: none;
    transform: none;
    transition:
      max-height 0.52s cubic-bezier(0.4, 0, 0.2, 1),
      opacity 0.36s ease,
      visibility 0s linear 0.52s;
  }

  .nav__item--dropdown.is-submenu-open .nav__sub {
    max-height: min(70vh, 22rem);
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
    transform: none;
    transition:
      max-height 0.52s cubic-bezier(0.4, 0, 0.2, 1),
      opacity 0.4s ease,
      visibility 0s;
  }

  .nav__item--dropdown.is-submenu-open > .nav__link .nav__caret {
    transform: rotate(180deg);
    transform-origin: 50% 35%;
  }

  .nav__sub a {
    padding: 0.4rem 0;
    opacity: 1;
    transform: none;
    transition: none;
  }

  .nav__item--dropdown > .nav__link .nav__caret {
    transition: transform 0.45s cubic-bezier(0.4, 0, 0.2, 1);
  }

  @media (prefers-reduced-motion: reduce) {
    .nav,
    .nav__sub,
    .nav__sub a,
    .nav__list > .nav__item,
    .nav .btn--header-cta,
    .lang-switch {
      transition: none;
      transform: none;
    }
  }

  .stats {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .gallery-grid {
    grid-template-columns: 1fr;
  }

  .contact-form {
    grid-template-columns: 1fr;
  }

  .faq__columns {
    grid-template-columns: 1fr;
    grid-template-rows: none;
  }

  .faq__col {
    display: flex;
    flex-direction: column;
    grid-row: auto;
  }
'''


def minify_css(src: str) -> str:
    out = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    out = re.sub(r"\s+", " ", out)
    out = re.sub(r"\s*([{}:;,>])\s*", r"\1", out)
    return out.replace(";}", "}").strip()


def main() -> None:
    core = CORE.read_text(encoding="utf-8")
    if MARKER in core:
        print("already present")
    else:
        # Insert before closing of the mobile services media query that has MOBILE_PSI_HERO_LAYOUT
        needle = "  .services .service-card__text {\n    font-size: clamp(0.82rem, 2.8vw, 0.95rem);\n    line-height: 1.25;\n  }\n}"
        if needle not in core:
            raise SystemExit("insert point not found")
        core = core.replace(
            needle,
            "  .services .service-card__text {\n    font-size: clamp(0.82rem, 2.8vw, 0.95rem);\n    line-height: 1.25;\n  }\n"
            + SHARED_MOBILE
            + "\n}",
            1,
        )
        CORE.write_text(core, encoding="utf-8")
        print("patched styles.css")

    # Rebuild min
    (ROOT / "css" / "styles.min.css").write_text(
        minify_css(CORE.read_text(encoding="utf-8")), encoding="utf-8"
    )
    (ROOT / "css" / "styles-pages.min.css").write_text(
        minify_css(PAGES.read_text(encoding="utf-8")), encoding="utf-8"
    )

    minc = (ROOT / "css" / "styles.min.css").read_text(encoding="utf-8")
    print("min has nav-toggle flex", "nav-toggle{display:flex" in minc)
    print("min max-width:900 count", minc.count("max-width:900"))
    print("min KB", round(len(minc) / 1024, 1))


if __name__ == "__main__":
    main()
