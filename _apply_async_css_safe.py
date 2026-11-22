# -*- coding: utf-8 -*-
"""
Defer stylesheets (shorten critical request chain) without FOUC jump:
- richer critical CSS aligned with final above-fold layout
- css-ready only after all site CSS files have loaded
- freeze transitions until css-ready
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CRITICAL = (
    ":root{--color-green:#51735e;--color-green-dark:#43604d;--color-gold:#c3b78e;--color-gold-hover:#b0a47c;"
    "--color-white:#fff;--color-off-white:#faf9f7;--color-text:#2b523a;--color-text-body:#234832;"
    "--header-nav-text:#2b523a;--header-lang:#2b523a;"
    "--font-serif:\"Gilda Display\",Georgia,serif;--font-sans:\"League Spartan\",system-ui,sans-serif;"
    "--font-gold-script:\"Dancing Script\",cursive;--fs-h1:clamp(2.5rem,1.55rem + 2.35vw,3.75rem);"
    "--fs-p:clamp(1.02rem,.96rem + .2vw,1.1rem);--fs-btn:.95rem;--fs-nav-bar:clamp(.95rem,.85rem + .25vw,1.1rem);"
    "--btn-pad-y:.62rem;--btn-pad-x:1.3rem;"
    "--fs-section-gold-accent:clamp(1.35rem,1.05rem + .55vw,1.7rem);--hero-content-max:clamp(28rem,52vw,42rem);"
    "--container:87.5rem;--section-inline:clamp(2.75rem,9.4vw,11.25rem);--section-space:clamp(3.35rem,2.6rem + 2.8vw,5.8rem);"
    "--header-h:clamp(4.25rem,3.8rem + .6vw,5rem);--header-outer-h:calc(var(--header-h) + 1px);"
    "--screen-fill:calc(var(--app-vh,100vh) - var(--header-outer-h));--radius:6px;--radius-sm:6px;--radius-card:6px}"
    "@supports (height:100svh){:root{--screen-fill:calc(var(--app-vh,100svh) - var(--header-outer-h))}}"
    "*,*::before,*::after{box-sizing:border-box}"
    "html{background-color:var(--color-off-white);font-size:16px;--layout-gutter:var(--section-inline);--page-gutter:var(--layout-gutter);"
    "scrollbar-gutter:stable;overflow-x:clip;max-width:100%}"
    "body{margin:0;font-family:var(--font-sans);font-weight:300;font-size:var(--fs-p);color:var(--color-text);"
    "background:var(--color-off-white);line-height:1.3;-webkit-font-smoothing:antialiased;overflow-x:clip}"
    "@media (max-width:480px){html{--layout-gutter:max(.75rem,4vw)}}"
    "@media (max-width:1024px) and (min-width:481px){html{--layout-gutter:clamp(1.35rem,4.2vw,3.75rem)}}"
    # Same position as in styles.css (before base rules) so the cascade matches exactly
    "@media (min-width:1025px) and (max-width:1439px){"
    ":root{--section-space:clamp(3.35rem,3.8vw,4.85rem);--hero-content-max:min(36rem,100%)}"
    ".hero__grid{grid-template-columns:minmax(0,1.12fr) minmax(0,.88fr)}"
    ".hero__content{padding-block:clamp(1.85rem,3.8vw,3.25rem);padding-right:clamp(1.1rem,2.8vw,2.25rem)}"
    ".hero__lead{margin-bottom:1.5rem;max-width:min(34rem,100%)}"
    ".hero__media{margin-left:clamp(-6.5rem,-11vw,-2rem)}"
    ".hero__image-bg,.page-hero__image-bg{left:clamp(18%,30vw,38%)}"
    "}"
    "@media (min-width:1025px) and (max-width:1280px){"
    ":root{--fs-section-gold-accent:clamp(1.3rem,1.1rem + .4vw,1.5rem)}"
    ".hero__grid{grid-template-columns:minmax(0,1.18fr) minmax(0,.82fr)}"
    ".nav{gap:clamp(.55rem,1.2vw,1rem)}.nav__list{gap:clamp(.4rem,1vw,.85rem)}.header__inner{gap:1rem}"
    "}"
    "@media (min-width:901px) and (max-height:820px){"
    ".hero__content{padding-block:clamp(1.35rem,3.5vh,2.35rem)}"
    ".hero__tagline{margin-bottom:.65rem}.hero__title{margin-bottom:.85rem}.hero__lead{margin-bottom:1.15rem}"
    "}"
    "img{max-width:100%;height:auto;display:block}"
    "a{color:inherit;text-decoration:none}"
    "h1{font-family:var(--font-serif);font-weight:400;font-size:var(--fs-h1);line-height:1.15;margin:0 0 .5em}"
    "p{font-size:var(--fs-p);font-weight:300!important;line-height:1.3!important;margin:0 0 1em}"
    # No animated reflow when full CSS arrives
    "html:not(.css-ready) *,html:not(.css-ready) *::before,html:not(.css-ready) *::after{transition:none!important;animation:none!important}"
    ".container{width:min(var(--container),calc(100% - (2 * var(--page-gutter))));margin-inline:auto}"
    ".site-header{position:sticky;top:0;z-index:10001;background:#fff;border-bottom:1px solid rgba(81,115,94,.1)}"
    ".header__inner{display:flex;align-items:center;justify-content:space-between;height:var(--header-h);min-height:var(--header-h);gap:1.5rem}"
    ".logo{display:inline-flex;align-items:center;flex-shrink:0;line-height:0;text-decoration:none}"
    ".logo img{height:clamp(3.1rem,5.4vw,3.85rem);width:auto;display:block}"
    ".nav-toggle{display:none;flex-direction:column;gap:6px;padding:8px;background:none;border:0;cursor:pointer}"
    ".nav-toggle span{display:block;width:24px;height:2px;background:var(--color-green)}"
    ".nav{display:flex;align-items:center;justify-content:flex-end;flex-wrap:nowrap;gap:clamp(1.15rem,2.2vw,1.75rem)}"
    ".nav__list{display:flex;flex-wrap:nowrap;align-items:center;gap:clamp(1rem,2vw,1.65rem);list-style:none;margin:0;padding:0}"
    ".nav__item{position:relative}"
    ".nav__link{display:inline-flex;align-items:center;white-space:nowrap;gap:.35rem;font-family:var(--font-sans);font-size:var(--fs-nav-bar);font-weight:400;letter-spacing:.01em;color:var(--header-nav-text)}"
    "@media (min-width:901px){.nav__link{padding-block:.2rem}}"
    ".nav__caret{display:inline-block;width:0;height:0;margin-top:.15em;border-left:3.5px solid transparent;"
    "border-right:3.5px solid transparent;border-top:4px solid var(--header-nav-text);flex-shrink:0}"
    "html:not(.css-ready) .nav__sub{display:none!important;opacity:0;visibility:hidden;pointer-events:none;"
    "transform:translateX(-50%) translateY(-8px)}"
    ".lang-switch{display:inline-flex;align-items:center;gap:.35rem;font-family:var(--font-sans);font-size:var(--fs-nav-bar);"
    "font-weight:500;color:var(--header-lang);margin-left:.15rem}"
    ".lang-switch__link{color:var(--header-lang);font-weight:700}"
    ".lang-switch__link--current{color:var(--color-gold)}"
    ".lang-switch__sep{opacity:.55;font-weight:400}"
    ".btn{display:inline-flex;align-items:center;justify-content:center;gap:.35em;padding:var(--btn-pad-y) var(--btn-pad-x);"
    "border:0;border-radius:var(--radius-sm);font-family:var(--font-sans);font-size:var(--fs-btn);font-weight:700;"
    "letter-spacing:.11em;line-height:1.2;text-decoration:none;text-transform:uppercase;cursor:pointer}"
    ".btn--gold,.btn--header-cta,.btn--hero-cta{background:var(--color-gold);color:#fff}"
    ".btn--hero-cta{align-self:flex-start}"
    ".btn--header-cta{padding:.5rem 1.15rem;border-radius:var(--radius-sm);white-space:nowrap;font-size:.9rem}"
    # Hero matches final CSS exactly — avoids image/layout jump when full CSS arrives
    ".hero{position:relative;min-height:var(--screen-fill);height:var(--screen-fill);display:flex;flex-direction:column;"
    "padding:0;overflow-x:clip;overflow-y:hidden;background:var(--color-white);box-sizing:border-box}"
    ".hero__grid{position:relative;z-index:1;flex:1;display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);"
    "align-items:stretch;min-height:0;width:100%;container-type:inline-size}"
    ".hero__content{display:flex;flex-direction:column;justify-content:center;box-sizing:border-box;"
    "margin-left:calc((100cqw - min(var(--container),calc(100cqw - 2 * var(--layout-gutter)))) / 2);"
    "padding-block:var(--section-space);padding-inline:0;padding-right:clamp(1.25rem,3.5vw,2.75rem);"
    "width:min(var(--hero-content-max),100%);justify-self:start;min-width:0;position:relative;z-index:2;"
    "background:linear-gradient(90deg,#fff 0%,#fff 58%,rgba(255,255,255,.9) 82%,rgba(255,255,255,0) 100%)}"
    ".hero__tagline{font-family:var(--font-gold-script);font-size:var(--fs-section-gold-accent);font-weight:500;"
    "color:var(--color-gold);margin:0 0 1rem;letter-spacing:.02em;line-height:1.35}"
    ".hero__title{color:var(--color-text);margin:0 0 1.25rem;letter-spacing:-.02em}"
    ".hero__lead{color:var(--color-text-body);margin:0 0 2rem;max-width:min(38rem,100%);font-size:var(--fs-p);line-height:1.3}"
    ".hero__media{position:relative;z-index:0;min-height:0;height:100%;display:flex;flex-direction:column;"
    "margin-left:clamp(-5.5rem,-9vw,-1.25rem)}"
    ".hero__image-wrap{position:relative;flex:1;min-height:0;width:100%;overflow:hidden;"
    "border-radius:var(--radius-card) 0 0 var(--radius-card);background:transparent}"
    ".hero__image-figure{position:relative;z-index:1;width:100%;height:100%;min-height:100%;max-width:none;"
    "object-fit:cover;object-position:center;display:block;pointer-events:none}"
    ".hero__image-bg{position:absolute;top:0;right:0;bottom:0;left:clamp(24%,36vw,42%);z-index:0;"
    "overflow:hidden;pointer-events:none;background:#e8ebe9;contain:layout paint}"
    ".hero__image-bg picture,.hero__image-bg img{position:absolute;inset:0;display:block;width:100%;height:100%;max-width:none}"
    ".hero__image-bg img{object-fit:cover;object-position:right center}"
    ".page-hero{--page-hero-pad-y:clamp(2.75rem,4vw,3.75rem);"
    "--page-hero-h:max(calc(var(--screen-fill)*0.36),calc(var(--page-hero-pad-y)*2 + 15rem));"
    "position:relative;min-height:var(--page-hero-h);height:auto;overflow:hidden;background:var(--color-white);display:flex;align-items:center}"
    ".page-hero__grid{position:relative;z-index:1;width:min(var(--container),calc(100% - (2 * var(--page-gutter))));margin-inline:auto}"
    ".page-hero__image-bg{position:absolute;top:0;right:0;bottom:0;left:clamp(24%,36vw,42%);z-index:0;"
    "overflow:hidden;pointer-events:none}"
    ".page-hero__image-bg img{position:absolute;top:auto;right:-.75rem;bottom:-2.25rem;left:auto;"
    "height:175%;width:auto;max-width:none;display:block}"
    ".page-hero__title{font-family:var(--font-serif);font-weight:400;font-size:var(--fs-h1);color:var(--color-text);margin:0 0 1rem}"
    ".page-hero__lead{color:var(--color-text-body);max-width:36rem;font-size:var(--fs-p);line-height:1.3;margin:0 0 1.5rem}"
    "@media (max-width:900px){"
    ".nav-toggle{display:flex}.nav{display:none}"
    ".hero{min-height:var(--screen-fill);height:var(--screen-fill)}"
    ".hero__grid{grid-template-columns:1fr;grid-template-rows:minmax(min(30vh,300px),auto);"
    "align-items:stretch;position:relative;z-index:1;isolation:isolate}"
    ".hero__image-bg{left:0;right:0;width:100%}"
    ".hero__image-bg img{inset:0;width:100%;height:100%;max-width:none;object-fit:cover;object-position:center}"
    ".hero__media{grid-row:1;grid-column:1;position:absolute;inset:0;margin-left:0;min-height:100%;height:100%;z-index:0}"
    '.hero__media::after{content:"";position:absolute;inset:0;z-index:2;'
    "background:rgba(18,17,13,.52);opacity:1;pointer-events:none}"
    ".hero__image-wrap{border-radius:0;min-height:100%;height:100%}"
    ".hero__image-figure{width:100%;height:100%;min-height:100%;object-fit:cover;object-position:center}"
    ".hero__content{grid-row:1;grid-column:1;"
    "margin-left:calc((100cqw - min(var(--container),calc(100cqw - 2 * var(--layout-gutter)))) / 2);"
    "margin-right:calc((100cqw - min(var(--container),calc(100cqw - 2 * var(--layout-gutter)))) / 2);"
    "width:min(var(--container),calc(100cqw - 2 * var(--layout-gutter)));max-width:100%;justify-self:stretch;"
    "position:relative;z-index:2;padding-block:clamp(2rem,6vw,3rem);padding-right:0;background:transparent}"
    ".hero__title{color:#fff}.hero__lead{color:rgba(255,255,255,.92)}"
    ".hero .hero__tagline{font-size:max(1rem,calc(var(--fs-section-gold-accent) * .92))}"
    ".hero .hero__title{font-size:clamp(2.1rem,5.4vw,3.05rem);line-height:1.14}"
    ".page-hero__image-bg{left:0;right:0;width:100%}"
    ".page-hero__image-bg img{top:0;right:auto;bottom:0;left:0;width:100%;height:100%;max-width:none;"
    "object-fit:cover;object-position:center}"
    "}"
    "@media (max-width:1200px) and (min-width:901px){"
    ".hero__media{margin-left:clamp(-7.5rem,-14vw,-2.75rem)}"
    ".hero__image-bg,.page-hero__image-bg{left:clamp(14%,26vw,34%)}"
    "}"
    # Partner logos: reserved box before decode
    ".partners__sequence{min-height:clamp(2.85rem,4.4vw,4rem)}"
    ".partners__logo{display:block;height:clamp(2.85rem,4.4vw,4rem);width:calc(clamp(2.85rem,4.4vw,4rem)*2.45);"
    "aspect-ratio:2.45/1;object-fit:contain}"
    "@media (max-width:640px){.partners__logo{height:clamp(2.4rem,8vw,3rem)}}"
)

CRITICAL_BLOCK_RE = re.compile(r"/\*critical\*/.*?(?=</style>)", re.S)

# Blocking or previous async chunks (script may be before or after links)
CSS_CHUNK_RE = re.compile(
    r"(?:[ \t]*<script>\(function\(d\)\{var left=\d+;[\s\S]*?</script>\s*)?"
    r"[ \t]*<link rel=\"(?:stylesheet|preload)\"[^>]*href=\"((?:\.\./)?css/styles\.min\.css)\"[^>]*>\s*"
    r"(?:<noscript><link rel=\"stylesheet\" href=\"(?:\.\./)?css/styles\.min\.css\"\s*/?></noscript>\s*)?"
    r"(?:[ \t]*<link rel=\"(?:stylesheet|preload)\"[^>]*href=\"((?:\.\./)?css/styles-pages\.min\.css)\"[^>]*>\s*"
    r"(?:<noscript><link rel=\"stylesheet\" href=\"(?:\.\./)?css/styles-pages\.min\.css\"\s*/?></noscript>\s*)?)?"
    r"(?:<script>document\.documentElement\.classList\.add\([\"']css-ready[\"']\);?</script>\s*)?"
    r"(?:<script>\(function\(d\)\{var hrefs=[\s\S]*?</script>\s*)?"
    r"(?:<script>!function\(d\)\{[\s\S]*?</script>\s*)?",
    re.I,
)


def css_loader_block(core_href: str, pages_href: str | None) -> str:
    hrefs = [core_href] + ([pages_href] if pages_href else [])
    n = len(hrefs)
    # Script FIRST so onload can call __cssReady even if cached/instant
    # Enable transitions only after layout has settled with full CSS
    # (double rAF), otherwise sections animate/jump from critical → final.
    boot = (
        "  <script>(function(d){"
        f"var left={n};"
        "function ready(){"
        "requestAnimationFrame(function(){requestAnimationFrame(function(){"
        "d.documentElement.classList.add('css-ready')"
        "})})}"
        "window.__cssReady=function(){if(left>0&&--left<=0)ready()};"
        "setTimeout(ready,2500);"
        "})(document);</script>\n"
    )
    links = []
    for href in hrefs:
        links.append(
            f'  <link rel="preload" href="{href}" as="style" '
            f'onload="this.onload=null;this.rel=\'stylesheet\';window.__cssReady&&window.__cssReady()" />'
        )
        links.append(f'  <noscript><link rel="stylesheet" href="{href}" /></noscript>')
    return boot + "\n".join(links) + "\n"


def is_redirect(text: str) -> bool:
    return 'http-equiv="refresh"' in text or "window.location.replace" in text


def fix_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if is_redirect(text) or "css/styles.min.css" not in text:
        # Still refresh critical if present on redirects? skip
        if "/*critical*/" in text:
            nt = CRITICAL_BLOCK_RE.sub(f"/*critical*/{CRITICAL}", text, count=1)
            if nt != text:
                path.write_text(nt, encoding="utf-8")
                return "critical-only"
        return "skip"

    if "/*critical*/" in text:
        text = CRITICAL_BLOCK_RE.sub(f"/*critical*/{CRITICAL}", text, count=1)

    m = CSS_CHUNK_RE.search(text)
    if not m:
        return "no-css-chunk"

    core = m.group(1)
    pages = m.group(2)
    # Home pages: never load pages CSS
    if path.name == "index.html":
        pages = None
    elif pages is None and path.name != "index.html":
        prefix = "../" if path.parent.name == "hu" else ""
        pages = f"{prefix}css/styles-pages.min.css"

    block = css_loader_block(core, pages)
    text = CSS_CHUNK_RE.sub(block, text, count=1)
    path.write_text(text, encoding="utf-8")
    return "updated"


def main() -> None:
    counts: dict[str, int] = {}
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        if path.name.startswith("preview"):
            continue
        status = fix_file(path)
        counts[status] = counts.get(status, 0) + 1
        if status in {"updated", "no-css-chunk"}:
            print(status, path.relative_to(ROOT), "pages" if path.name != "index.html" else "home")
    print("summary", counts)


if __name__ == "__main__":
    main()
