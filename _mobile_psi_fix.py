# -*- coding: utf-8 -*-
"""Mobile-only PSI fixes: smaller WebPs, HTML srcset/preload, CLS CSS. Desktop sources untouched."""
from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent
IMGS = ROOT / "assets" / "imgs"


def minify_css(src: str) -> str:
    out = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    out = re.sub(r"\s+", " ", out)
    out = re.sub(r"\s*([{}:;,>])\s*", r"\1", out)
    return out.replace(";}", "}").strip()


def resize_to_width(im: Image.Image, width: int) -> Image.Image:
    w, h = im.size
    if w <= width:
        return im
    nh = max(1, int(round(h * (width / w))))
    return im.resize((width, nh), Image.Resampling.LANCZOS)


def save_webp(
    src: Path,
    dest: Path,
    *,
    width: int | None = None,
    max_side: int | None = None,
    quality: int = 72,
    keep_alpha: bool = False,
    sharpen: bool = True,
) -> None:
    im = Image.open(src)
    if keep_alpha:
        im = im.convert("RGBA")
    else:
        if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
            rgba = im.convert("RGBA")
            bg = Image.new("RGB", rgba.size, (250, 249, 247))
            bg.paste(rgba, mask=rgba.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")

    if width:
        im = resize_to_width(im, width)
    elif max_side:
        w, h = im.size
        scale = min(1.0, max_side / max(w, h))
        if scale < 1:
            im = im.resize(
                (max(1, int(w * scale)), max(1, int(h * scale))),
                Image.Resampling.LANCZOS,
            )

    if sharpen and im.mode in ("RGB", "RGBA"):
        im = im.filter(ImageFilter.UnsharpMask(radius=0.9, percent=65, threshold=2))

    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=quality, method=6)
    print(
        f"{dest.relative_to(IMGS)}: {dest.stat().st_size/1024:.1f} KiB {im.size}"
    )


def generate_images() -> None:
    # Hero figure — mobile max 800 (no 1200 as 2x). Recompress.
    save_webp(
        IMGS / "Hero_img.png",
        IMGS / "Hero_img-800.webp",
        width=800,
        quality=70,
        keep_alpha=True,
        sharpen=True,
    )
    # Hero background — mobile max 900 (drop 1400 2x). Recompress.
    save_webp(
        IMGS / "Hero_background_img.png",
        IMGS / "Hero_background_img-900.webp",
        width=900,
        quality=68,
        keep_alpha=True,
        sharpen=True,
    )
    # Portrait — mobile only 600
    save_webp(
        IMGS / "Main_Rolam.jpg",
        IMGS / "Main_Rolam-600.webp",
        width=600,
        quality=70,
        keep_alpha=False,
        sharpen=True,
    )
    # Partner logo compression
    for name in ("Alveola.webp", "JB_lashes.webp"):
        src = IMGS / "Logo_Carousel" / name
        if not src.exists():
            continue
        im = Image.open(src).convert("RGBA")
        # Keep display height ~80–160px worth; re-encode smaller
        w, h = im.size
        if w > 220:
            im = resize_to_width(im, 220)
        dest = src
        im.save(dest, "WEBP", quality=70, method=6)
        print(f"Logo_Carousel/{name}: {dest.stat().st_size/1024:.1f} KiB {im.size}")

    # Gallery 400w for every existing -640.webp sibling
    for path_640 in IMGS.joinpath("page-gallery").rglob("*-640.webp"):
        stem = path_640.name.replace("-640.webp", "")
        full = path_640.with_name(stem + ".webp")
        jpg = path_640.with_name(stem + ".jpg")
        png = path_640.with_name(stem + ".png")
        src = full if full.exists() else (jpg if jpg.exists() else png)
        if not src or not src.exists():
            print("skip no src", path_640)
            continue
        dest = path_640.with_name(stem + "-400.webp")
        save_webp(
            src,
            dest,
            width=400,
            quality=68,
            keep_alpha=False,
            sharpen=True,
        )


HERO_IMG_BASE_CSS = """
.hero__image-bg::after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 1;
  background: rgba(255, 255, 255, 0.19);
  pointer-events: none;
}

.hero__image-bg img {
  position: absolute;
  top: 0;
  right: 0;
  left: auto;
  height: 100%;
  width: auto;
  max-width: none;
  object-fit: cover;
  object-position: right center;
  display: block;
  transition: transform 0.55s cubic-bezier(0.22, 1, 0.36, 1);
}
"""

HERO_MOBILE_CSS = """
  /* Home hero mobile — must live in core CSS (home does not load pages CSS) */
  .hero {
    --hero-mobile-overlay: rgba(18, 17, 13, 0.52);
    min-height: var(--screen-fill);
  }

  .hero__image-bg {
    left: 0;
    right: 0;
    width: 100%;
  }

  .hero__image-bg img {
    left: 0;
    right: 0;
    width: 100%;
    height: 100%;
    max-width: none;
    object-fit: cover;
    object-position: center center;
  }

  .hero__grid {
    grid-template-columns: 1fr;
    grid-template-rows: minmax(min(30vh, 300px), auto);
    align-items: stretch;
    position: relative;
    z-index: 1;
    isolation: isolate;
  }

  .hero__media {
    grid-row: 1;
    grid-column: 1;
    order: 0;
    position: absolute;
    inset: 0;
    margin-left: 0;
    min-height: 100%;
    height: 100%;
    z-index: 0;
  }

  .hero__media::after {
    opacity: 1;
  }

  .hero__image-wrap {
    border-radius: 0;
    min-height: 100%;
    height: 100%;
  }

  .hero__image-figure {
    position: relative;
    z-index: 1;
    width: 100%;
    height: 100%;
    min-height: 100%;
    object-fit: cover;
    object-position: center center;
  }

  .hero__content {
    grid-row: 1;
    grid-column: 1;
    margin-left: calc(
      (
          100cqw - min(var(--container), calc(100cqw - 2 * var(--layout-gutter)))
        ) /
        2
    );
    margin-right: calc(
      (
          100cqw - min(var(--container), calc(100cqw - 2 * var(--layout-gutter)))
        ) /
        2
    );
    width: min(var(--container), calc(100cqw - 2 * var(--layout-gutter)));
    max-width: 100%;
    justify-self: stretch;
    position: relative;
    z-index: 2;
    padding-block: clamp(2rem, 6vw, 3rem);
    padding-right: 0;
    background: transparent;
  }

  .hero .hero__tagline {
    font-size: max(1rem, calc(var(--fs-section-gold-accent) * 0.92));
  }

  .hero__title {
    color: var(--color-white);
  }

  .hero .hero__title {
    font-size: clamp(2.1rem, 5.4vw, 3.05rem);
    line-height: 1.14;
  }

  .hero__lead {
    color: rgba(255, 255, 255, 0.92);
  }

  .hero .hero__lead {
    font-size: var(--fs-p);
    line-height: 1.3;
  }

  /* CLS: reserve space for icons / partner logos before decode */
  .service-card__icon {
    width: clamp(2.25rem, 8vw, 3rem);
    height: clamp(2.25rem, 8vw, 3rem);
    aspect-ratio: 1 / 1;
  }

  .service-card__icon img,
  .services .service-card__icon img {
    width: 100%;
    height: 100%;
    max-width: none;
    aspect-ratio: 1 / 1;
    object-fit: contain;
  }

  .partners__logo {
    aspect-ratio: 2.75 / 1;
    width: auto;
    height: var(--partners-logo-h);
    max-width: min(13rem, 46vw);
  }
"""


def patch_styles_css() -> None:
    path = ROOT / "css" / "styles.css"
    text = path.read_text(encoding="utf-8")

    if ".hero__image-bg img {" not in text.split(".hero__image-bg {")[1][:800]:
        # Insert after .hero__image-bg { ... } block
        marker = "/* Háttér: jobb oldalról a szöveg alá tolódik szűküléskor */\n.hero__image-bg {"
        idx = text.find(marker)
        if idx < 0:
            raise SystemExit("hero__image-bg block not found")
        # find end of that rule
        brace = text.find("{", idx)
        depth = 0
        end = brace
        for i, ch in enumerate(text[brace:], brace):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if "MOBILE_PSI_HERO_BASE" not in text:
            insert = (
                "\n\n/* MOBILE_PSI_HERO_BASE: required on home (pages CSS not loaded) */"
                + HERO_IMG_BASE_CSS
            )
            text = text[:end] + insert + text[end:]

    # Inject mobile hero into first @media (max-width: 900px) that has services rules
    if "MOBILE_PSI_HERO_LAYOUT" not in text:
        m = re.search(
            r"@media \(max-width: 900px\) \{\s*\n\s*\.references,",
            text,
        )
        if not m:
            raise SystemExit("mobile 900 services media not found")
        # insert after opening brace of that media query
        brace_pos = text.find("{", m.start())
        text = (
            text[: brace_pos + 1]
            + "\n  /* MOBILE_PSI_HERO_LAYOUT */"
            + HERO_MOBILE_CSS
            + text[brace_pos + 1 :]
        )

    path.write_text(text, encoding="utf-8")
    print("patched styles.css")


def patch_html() -> None:
    html_files = list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html"))
    n = 0
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        orig = text
        prefix = "../" if path.parent.name == "hu" else ""

        # Mobile hero bg: only 900 (no 1400 2x)
        text = re.sub(
            r'(media="\(max-width: 900px\)" type="image/webp" srcset=")'
            r'((?:\.\./)?assets/imgs/Hero_background_img)-900\.webp 1x, '
            r'(?:\.\./)?assets/imgs/Hero_background_img-1400\.webp 2x"',
            rf'\1\2-900.webp"',
            text,
        )

        # Mobile hero figure: only 800
        text = re.sub(
            r'(media="\(max-width: 900px\)" type="image/webp" srcset=")'
            r'((?:\.\./)?assets/imgs/Hero_img)-800\.webp 1x, '
            r'(?:\.\./)?assets/imgs/Hero_img-1200\.webp 2x"',
            rf'\1\2-800.webp"',
            text,
        )

        # Mobile portrait: only 600
        text = re.sub(
            r'(media="\(max-width: 900px\)" type="image/webp" srcset=")'
            r'((?:\.\./)?assets/imgs/Main_Rolam)-600\.webp 1x, '
            r'(?:\.\./)?assets/imgs/Main_Rolam-900\.webp 2x"',
            rf'\1\2-600.webp"',
            text,
        )

        # Gallery: add 400w + tighten sizes so mobile prefers 400
        def gallery_srcset(m: re.Match[str]) -> str:
            pre = m.group(1)
            base = m.group(2)  # path without -640.webp
            rest = m.group(3)
            return (
                f'{pre}{base}-400.webp 400w, {base}-640.webp 640w, {rest}"'
            )

        text = re.sub(
            r'(srcset=")((?:\.\./)?assets/imgs/page-gallery/[^"]+?)-640\.webp 640w, '
            r'((?:\.\./)?assets/imgs/page-gallery/[^"]+?\.webp 1200w)"',
            gallery_srcset,
            text,
        )
        text = text.replace(
            'sizes="(max-width: 900px) 45vw, 280px"',
            'sizes="(max-width: 900px) 42vw, 280px"',
        )

        # fetchpriority + decoding on hero background img (LCP on mobile)
        text = re.sub(
            r'(src="(?:\.\./)?assets/imgs/Hero_background_img\.png" alt="" width="1200" height="800" loading="eager")'
            r'(?: decoding="async")?(?: fetchpriority="high")?',
            r'\1 decoding="async" fetchpriority="high"',
            text,
        )

        # Home preload: mobile LCP = background; desktop = figure
        if path.name == "index.html":
            old_preload = re.search(
                r'[ \t]*<link rel="preload" as="image"[^>]*Hero_img[^>]*>\s*',
                text,
            )
            if old_preload:
                if path.parent.name == "hu":
                    new_pre = (
                        f'    <link rel="preload" as="image" type="image/webp" '
                        f'href="../assets/imgs/Hero_background_img-900.webp" '
                        f'media="(max-width: 900px)" fetchpriority="high" />\n'
                        f'    <link rel="preload" as="image" type="image/webp" '
                        f'href="../assets/imgs/Hero_img.webp" '
                        f'media="(min-width: 901px)" fetchpriority="high" />\n'
                    )
                else:
                    new_pre = (
                        f'    <link rel="preload" as="image" type="image/webp" '
                        f'href="assets/imgs/Hero_background_img-900.webp" '
                        f'media="(max-width: 900px)" fetchpriority="high" />\n'
                        f'    <link rel="preload" as="image" type="image/webp" '
                        f'href="assets/imgs/Hero_img.webp" '
                        f'media="(min-width: 901px)" fetchpriority="high" />\n'
                    )
                text = text[: old_preload.start()] + new_pre + text[old_preload.end() :]

            # Figure: drop fetchpriority high on mobile LCP competition — keep eager
            text = re.sub(
                r'(class="hero__image-figure"[^>]*?) fetchpriority="high"',
                r"\1",
                text,
            )
            # Ensure figure still has decoding async
            if 'class="hero__image-figure"' in text and 'fetchpriority="high"' in text:
                # only remove from figure specifically
                text = re.sub(
                    r'(<img\s+class="hero__image-figure"[^>]*?)(\s*fetchpriority="high")',
                    r"\1",
                    text,
                    count=1,
                )

        if text != orig:
            path.write_text(text, encoding="utf-8")
            n += 1
            print("html", path.relative_to(ROOT))
    print("html files updated", n)


def minify() -> None:
    css = ROOT / "css" / "styles.css"
    (ROOT / "css" / "styles.min.css").write_text(
        minify_css(css.read_text(encoding="utf-8")), encoding="utf-8"
    )
    pages = ROOT / "css" / "styles-pages.css"
    (ROOT / "css" / "styles-pages.min.css").write_text(
        minify_css(pages.read_text(encoding="utf-8")), encoding="utf-8"
    )
    print(
        "min CSS",
        round((ROOT / "css" / "styles.min.css").stat().st_size / 1024, 1),
        "KiB",
    )


def main() -> None:
    generate_images()
    patch_styles_css()
    patch_html()
    minify()
    print("done — re-inject critical CSS separately if needed")


if __name__ == "__main__":
    main()
