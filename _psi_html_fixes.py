# -*- coding: utf-8 -*-
"""Apply PageSpeed HTML fixes across all pages (bootstrap removal, webp, fonts)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

BOOTSTRAP_RE = re.compile(
    r'\s*<link rel="stylesheet" href="https://cdn\.jsdelivr\.net/npm/bootstrap@5\.3\.3/dist/css/bootstrap-(?:grid|utilities)\.min\.css"\s*/?>',
    re.I,
)

FONT_BLOCK_RE = re.compile(
    r'<link rel="preconnect" href="https://fonts\.googleapis\.com"\s*/?>\s*'
    r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin\s*/?>\s*'
    r'<link\s+href="https://fonts\.googleapis\.com/css2\?[^"]+"\s+rel="stylesheet"\s*/?>',
    re.I | re.S,
)

FONT_ASYNC = """<link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;500;600;700&family=Gilda+Display&family=League+Spartan:wght@300;400;500;600;700&display=swap" />
  <link
    href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;500;600;700&family=Gilda+Display&family=League+Spartan:wght@300;400;500;600;700&display=swap"
    rel="stylesheet"
    media="print"
    onload="this.media='all'"
  />
  <noscript>
    <link
      href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;500;600;700&family=Gilda+Display&family=League+Spartan:wght@300;400;500;600;700&display=swap"
      rel="stylesheet"
    />
  </noscript>"""


def hero_picture(src_prefix: str, kind: str) -> str:
    """kind: figure | bg"""
    if kind == "figure":
        return (
            f'<picture>\n'
            f'              <source type="image/webp" srcset="{src_prefix}Hero_img.webp" />\n'
            f'              <img\n'
            f'              class="hero__image-figure"\n'
            f'              fetchpriority="high"\n'
            f'              decoding="async"\n'
            f'              src="{src_prefix}Hero_img.jpg"\n'
            f'              alt="Gästin bei der Gesichtsbehandlung"\n'
            f'              width="960"\n'
            f'              height="640"\n'
            f'              loading="eager"\n'
            f'            />\n'
            f'            </picture>'
        )
    return (
        f'<picture>\n'
        f'          <source type="image/webp" srcset="{src_prefix}Hero_background_img.webp" />\n'
        f'          <img src="{src_prefix}Hero_background_img.jpg" alt="" width="1200" height="800" loading="eager" decoding="async" />\n'
        f'        </picture>'
    )


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    depth = 0 if path.parent == ROOT else path.parent.relative_to(ROOT).as_posix().count("/") + (0 if "hu" not in path.parts else 0)
    # asset prefix
    if path.parent == ROOT:
        prefix = "assets/imgs/"
        logo_prefix = "assets/imgs/Logo_Carousel/"
    elif path.parent.name == "hu":
        prefix = "../assets/imgs/"
        logo_prefix = "../assets/imgs/Logo_Carousel/"
    else:
        prefix = "assets/imgs/"
        logo_prefix = "assets/imgs/Logo_Carousel/"

    text = BOOTSTRAP_RE.sub("", text)

    if FONT_BLOCK_RE.search(text):
        text = FONT_BLOCK_RE.sub(FONT_ASYNC, text, count=1)

    # Preload LCP webp (home pages only)
    if path.name in ("index.html",) and "Hero_img.webp" not in text.split("preload")[0] if False else True:
        if 'rel="preload" as="image"' not in text and "Hero_img" in text:
            preload = (
                f'  <link rel="preload" as="image" type="image/webp" href="{prefix}Hero_img.webp" fetchpriority="high" />\n'
            )
            text = text.replace(
                '<link rel="stylesheet" href="css/styles.css" />',
                preload + '  <link rel="stylesheet" href="css/styles.css" />',
                1,
            )
            text = text.replace(
                '<link rel="stylesheet" href="../css/styles.css" />',
                preload + '  <link rel="stylesheet" href="../css/styles.css" />',
                1,
            )

    # Hero figure PNG → picture/webp
    text = re.sub(
        r'<img\s+class="hero__image-figure"\s+fetchpriority="high"\s+decoding="async"\s+src="(?:\.\./)?assets/imgs/Hero_img\.png"[^>]*>',
        lambda m: (
            f'<picture>\n'
            f'              <source type="image/webp" srcset="{prefix}Hero_img.webp" />\n'
            f'              <img\n'
            f'              class="hero__image-figure"\n'
            f'              fetchpriority="high"\n'
            f'              decoding="async"\n'
            f'              src="{prefix}Hero_img.jpg"\n'
            f'              alt="' + (re.search(r'alt="([^"]*)"', m.group(0)).group(1) if re.search(r'alt="([^"]*)"', m.group(0)) else "") + '"\n'
            f'              width="960"\n'
            f'              height="640"\n'
            f'              loading="eager"\n'
            f'            />\n'
            f'            </picture>'
        ),
        text,
        count=1,
        flags=re.S,
    )

    # Simpler replacements for remaining hero refs
    text = text.replace(f'{prefix}Hero_img.png', f'{prefix}Hero_img.webp')
    text = text.replace("assets/imgs/Hero_img.png", f"{prefix}Hero_img.webp" if path.parent.name == "hu" else "assets/imgs/Hero_img.webp")
    text = text.replace("../assets/imgs/Hero_img.png", "../assets/imgs/Hero_img.webp")

    # Background hero
    text = re.sub(
        r'(<div class="hero__image-bg"[^>]*>\s*)<img src="(?:\.\./)?assets/imgs/Hero_background_img\.png"([^>]*)>',
        rf'\1<picture><source type="image/webp" srcset="{prefix}Hero_background_img.webp" /><img src="{prefix}Hero_background_img.jpg"\2></picture>',
        text,
        count=1,
        flags=re.S,
    )
    text = text.replace("Hero_background_img.png", "Hero_background_img.webp")

    # Page-hero backgrounds (subpages)
    text = text.replace("Hero_background_img.webp.webp", "Hero_background_img.webp")

    # Logo carousel png → webp
    for logo in ("Alveola", "Callux", "GiGi", "JB_lashes", "LN", "Long_lashes", "perfect_nails", "RefectoCil", "Studex"):
        text = text.replace(f"Logo_Carousel/{logo}.png", f"Logo_Carousel/{logo}.webp")

    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        if path.name.startswith("preview"):
            continue
        if fix_file(path):
            changed.append(str(path.relative_to(ROOT)))
    print("updated", len(changed))
    for c in changed:
        print(" ", c)


if __name__ == "__main__":
    main()
