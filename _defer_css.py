# -*- coding: utf-8 -*-
"""Defer styles.min.css (non-blocking) + inject compact critical CSS in <head>."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Compact critical first-paint CSS (header + hero/page-hero + tokens)
CRITICAL = (
    ":root{--color-green:#51735e;--color-green-dark:#43604d;--color-gold:#c3b78e;--color-gold-hover:#b0a47c;"
    "--color-white:#fff;--color-off-white:#faf9f7;--color-text:#2b523a;--color-text-body:#234832;"
    "--font-serif:\"Gilda Display\",Georgia,serif;--font-sans:\"League Spartan\",system-ui,sans-serif;"
    "--font-gold-script:\"Dancing Script\",cursive;--fs-h1:clamp(2.5rem,1.55rem + 2.35vw,3.75rem);"
    "--fs-p:clamp(1.02rem,.96rem + .2vw,1.1rem);--fs-btn:.95rem;--btn-pad-y:.62rem;--btn-pad-x:1.3rem;"
    "--fs-section-gold-accent:clamp(1.35rem,1.05rem + .55vw,1.7rem);--hero-content-max:clamp(28rem,52vw,42rem);"
    "--container:87.5rem;--section-inline:clamp(2.75rem,9.4vw,11.25rem);--section-space:clamp(3.35rem,2.6rem + 2.8vw,5.8rem);"
    "--header-h:clamp(4.25rem,3.8rem + .6vw,5rem);--header-outer-h:calc(var(--header-h) + 1px);"
    "--screen-fill:calc(var(--app-vh,100vh) - var(--header-outer-h));--radius:6px;--radius-sm:6px;--radius-card:6px}"
    "@supports (height:100svh){:root{--screen-fill:calc(var(--app-vh,100svh) - var(--header-outer-h))}}"
    "*,*::before,*::after{box-sizing:border-box}"
    "html{background-color:var(--color-off-white);font-size:16px;--layout-gutter:var(--section-inline);--page-gutter:var(--layout-gutter)}"
    "body{margin:0;font-family:var(--font-sans);color:var(--color-text);background:var(--color-off-white);line-height:1.45;-webkit-font-smoothing:antialiased}"
    "img{max-width:100%;height:auto;display:block}"
    "a{color:inherit}"
    "h1{font-family:var(--font-serif);font-weight:400;font-size:var(--fs-h1);line-height:1.15;margin:0}"
    "p{margin:0}"
    ".container{width:min(var(--container),calc(100% - (2 * var(--page-gutter))));margin-inline:auto}"
    ".site-header{position:sticky;top:0;z-index:10001;background:#fff;border-bottom:1px solid rgba(81,115,94,.1)}"
    ".header__inner{display:flex;align-items:center;justify-content:space-between;height:var(--header-h);min-height:var(--header-h);gap:1.5rem}"
    ".logo{display:inline-flex;align-items:center;line-height:0;text-decoration:none}"
    ".logo img{height:clamp(3.1rem,5.4vw,3.85rem);width:auto}"
    ".nav-toggle{display:none}"
    # Hide submenu until deferred CSS loads (avoids flash + slide-away)
    "html:not(.css-ready) .nav__sub{display:none!important;opacity:0;visibility:hidden;pointer-events:none;"
    "transform:translateX(-50%) translateY(-8px)}"
    ".btn{display:inline-flex;align-items:center;justify-content:center;gap:.35rem;padding:var(--btn-pad-y) var(--btn-pad-x);"
    "border:0;border-radius:var(--radius-sm);font:inherit;font-size:var(--fs-btn);font-weight:600;letter-spacing:.04em;"
    "text-decoration:none;text-transform:uppercase;cursor:pointer}"
    ".btn--gold{background:var(--color-gold);color:#fff}"
    ".btn--header-cta{background:var(--color-gold);color:#fff;padding:.5rem 1.15rem;border-radius:var(--radius-sm);white-space:nowrap;font-size:.9rem}"
    ".hero{position:relative;min-height:var(--screen-fill);height:var(--screen-fill);overflow:hidden;background:var(--color-white);container-type:inline-size}"
    ".hero__grid{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);align-items:stretch;min-height:var(--screen-fill);height:100%}"
    ".hero__content{display:flex;flex-direction:column;justify-content:center;padding-block:var(--section-space);padding-right:clamp(1.25rem,3.5vw,2.75rem);"
    "width:min(var(--hero-content-max),100%);position:relative;z-index:2;"
    "background:linear-gradient(90deg,#fff 0%,#fff 58%,rgba(255,255,255,.9) 82%,rgba(255,255,255,0) 100%)}"
    ".hero__tagline{font-family:var(--font-gold-script);font-size:var(--fs-section-gold-accent);font-weight:500;color:var(--color-gold);margin:0 0 1rem}"
    ".hero__title{color:var(--color-text);margin:0 0 1.25rem;letter-spacing:-.02em}"
    ".hero__lead{color:var(--color-text-body);margin:0 0 2rem;max-width:min(38rem,100%);font-size:var(--fs-p);line-height:1.3}"
    ".hero__media{position:relative;min-height:0;height:100%;display:flex;flex-direction:column;margin-left:clamp(-5.5rem,-9vw,-1.25rem)}"
    ".hero__image-wrap{position:relative;flex:1;min-height:0;width:100%;overflow:hidden;border-radius:var(--radius-card) 0 0 var(--radius-card)}"
    ".hero__image-figure{width:100%;height:100%;min-height:100%;object-fit:cover;object-position:center;display:block}"
    ".hero__image-bg{position:absolute;top:0;right:0;bottom:0;left:clamp(24%,36vw,42%);z-index:0;overflow:hidden;pointer-events:none}"
    ".hero__image-bg img{position:absolute;top:0;right:0;height:100%;width:auto;max-width:none;object-fit:cover;object-position:right center}"
    ".page-hero{--page-hero-pad-y:clamp(2.75rem,4vw,3.75rem);"
    "--page-hero-h:max(calc(var(--screen-fill)*0.36),calc(var(--page-hero-pad-y)*2 + 15rem));"
    "position:relative;min-height:var(--page-hero-h);height:auto;overflow:hidden;background:var(--color-white);display:flex;align-items:center}"
    ".page-hero__grid{position:relative;z-index:1;width:min(var(--container),calc(100% - (2 * var(--page-gutter))));margin-inline:auto}"
    ".page-hero__title{font-family:var(--font-serif);font-weight:400;font-size:var(--fs-h1);color:var(--color-text);margin:0 0 1rem}"
    ".page-hero__lead{color:var(--color-text-body);max-width:36rem;font-size:var(--fs-p);line-height:1.3;margin:0 0 1.5rem}"
    "@media (max-width:900px){.nav-toggle{display:flex}.nav{display:none}.hero__grid{grid-template-columns:1fr}"
    ".hero__content{width:100%;padding-inline:var(--page-gutter);background:transparent}.hero__media{margin-left:0}}"
)

LANG_STYLE_RE = re.compile(
    r"(<style>)(html\{background-color:#faf9f7.*?</style>)",
    re.S,
)

CSS_LINK_RE = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(\.\./)?css/styles\.min\.css"\s*/?>\s*',
    re.I,
)


def async_css_block(prefix: str) -> str:
    """Non-blocking CSS; prefer _apply_async_css_safe.py for full site updates."""
    href = f"{prefix}css/styles.min.css"
    return (
        f'  <script>(function(d){{var left=1;function ready(){{d.documentElement.classList.add("css-ready")}}'
        f'window.__cssReady=function(){{if(left>0&&--left<=0)ready()}};setTimeout(ready,2500);}})(document);</script>\n'
        f'  <link rel="preload" href="{href}" as="style" '
        f'onload="this.onload=null;this.rel=\'stylesheet\';window.__cssReady&&window.__cssReady()" />\n'
        f'  <noscript><link rel="stylesheet" href="{href}" /></noscript>\n'
    )


CRITICAL_BLOCK_RE = re.compile(
    r"/\*critical\*/.*?(?=</style>)",
    re.S,
)

# Full deferred CSS block (preload + noscript + fallback script)
PRELOAD_CSS_RE = re.compile(
    r'[ \t]*<link rel="preload" href="((?:\.\./)?css/styles\.min\.css)" as="style"[^>]*>\s*'
    r'<noscript><link rel="stylesheet" href="(?:\.\./)?css/styles\.min\.css"\s*/?></noscript>\s*'
    r'<script>!function\(d\)\{var l=d\.querySelector\(\'link\[rel=preload\]\[as=style\]\[href="(?:\.\./)?css/styles\.min\.css"\]\'\);.*?</script>\s*',
    re.S | re.I,
)


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    prefix = "../" if path.parent.name == "hu" else ""

    # Inject or refresh critical CSS in existing early <style> block
    def inject_critical(m: re.Match[str]) -> str:
        open_tag, body = m.group(1), m.group(2)
        if body.rstrip().endswith("</style>"):
            inner = body[: body.rfind("</style>")]
            if "/*critical*/" in inner or "--hero-content-max" in inner:
                # Refresh critical block contents
                if "/*critical*/" in inner:
                    inner = CRITICAL_BLOCK_RE.sub(f"/*critical*/{CRITICAL}", inner, count=1)
                else:
                    # Old inject without marker — append refreshed critical
                    inner = re.sub(
                        r":root\{--color-green:#51735e;.*?@media \(max-width:900px\)\{[^}]+\}\}",
                        f"/*critical*/{CRITICAL}",
                        inner,
                        count=1,
                        flags=re.S,
                    )
                return f"{open_tag}{inner}</style>"
            return f"{open_tag}{inner}/*critical*/{CRITICAL}</style>"
        return m.group(0)

    text2, n = LANG_STYLE_RE.subn(inject_critical, text, count=1)
    if n:
        text = text2
    elif "/*critical*/" not in text:
        text = text.replace(
            '<meta charset="UTF-8" />',
            f'<meta charset="UTF-8" />\n  <style>/*critical*/{CRITICAL}</style>',
            1,
        )
    elif "/*critical*/" in text:
        text = CRITICAL_BLOCK_RE.sub(f"/*critical*/{CRITICAL}", text, count=1)

    # Replace blocking stylesheet OR refresh already-deferred preload block
    if CSS_LINK_RE.search(text):
        text = CSS_LINK_RE.sub(async_css_block(prefix), text, count=1)
    elif PRELOAD_CSS_RE.search(text):
        text = PRELOAD_CSS_RE.sub(lambda m: async_css_block("" if m.group(1).startswith("css/") else "../"), text, count=1)
    elif f'href="{prefix}css/styles.min.css"' in text and 'as="style"' in text:
        # Already deferred with different markup — only ensure css-ready onload
        text = text.replace(
            "onload=\"this.onload=null;this.rel='stylesheet'\"",
            "onload=\"this.onload=null;this.rel='stylesheet';document.documentElement.classList.add('css-ready')\"",
        )
    elif "http-equiv=\"refresh\"" in text or "window.location.replace" in text:
        pass  # redirect stubs
    else:
        print("NO CSS LINK", path)

    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated = 0
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        if path.name.startswith("preview"):
            continue
        if fix_file(path):
            updated += 1
            print("updated", path.relative_to(ROOT))
    print("done", updated)


if __name__ == "__main__":
    main()
