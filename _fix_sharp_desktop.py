# -*- coding: utf-8 -*-
"""
Restore desktop sharpness for hero + Rólam images.
Mobile keeps small WebP; desktop always gets full-resolution source (no undersized srcset).
"""
from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent
IMGS = ROOT / "assets" / "imgs"


def save_webp_full(src: Path, dest: Path, *, quality: int, keep_alpha: bool, max_side: int | None = None) -> None:
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
    if max_side:
        w, h = im.size
        m = max(w, h)
        if m > max_side:
            s = max_side / m
            im = im.resize((max(1, int(w * s)), max(1, int(h * s))), Image.Resampling.LANCZOS)
            im = im.filter(ImageFilter.UnsharpMask(radius=0.8, percent=45, threshold=2))
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=quality, method=6)
    print(f"{dest.name}: {im.size} {dest.stat().st_size/1024:.0f}KB q={quality}")


def regenerate_masters() -> None:
    # Higher quality full heroes (desktop)
    if (IMGS / "Hero_img.png").exists():
        save_webp_full(IMGS / "Hero_img.png", IMGS / "Hero_img.webp", quality=95, keep_alpha=True)
    if (IMGS / "Hero_background_img.png").exists():
        save_webp_full(
            IMGS / "Hero_background_img.png",
            IMGS / "Hero_background_img.webp",
            quality=93,
            keep_alpha=True,
        )
    if (IMGS / "Main_Rolam.jpg").exists():
        save_webp_full(IMGS / "Main_Rolam.jpg", IMGS / "Main_Rolam.webp", quality=92, keep_alpha=False)
    if (IMGS / "Rolam_main.jpg").exists():
        save_webp_full(IMGS / "Rolam_main.jpg", IMGS / "Rolam_main.webp", quality=92, keep_alpha=False)
        # mobile variants
        save_webp_full(
            IMGS / "Rolam_main.jpg",
            IMGS / "Rolam_main-600.webp",
            quality=88,
            keep_alpha=False,
            max_side=600,
        )
        save_webp_full(
            IMGS / "Rolam_main.jpg",
            IMGS / "Rolam_main-900.webp",
            quality=90,
            keep_alpha=False,
            max_side=900,
        )

    # Rólam masonry: full webp ≈ original pixels (not capped at 1200 long side wrongly)
    for jpg in sorted((IMGS / "page-gallery" / "rolam").glob("*.jpg")):
        save_webp_full(jpg, jpg.with_suffix(".webp"), quality=91, keep_alpha=False)


def picture_mobile_desktop(
    prefix: str,
    *,
    mobile_1x: str,
    mobile_2x: str | None,
    desktop_webp: str,
    img_tag: str,
) -> str:
    """img_tag is full <img ...> without surrounding picture."""
    if mobile_2x:
        mob = f'{prefix}{mobile_1x} 1x, {prefix}{mobile_2x} 2x'
    else:
        mob = f"{prefix}{mobile_1x}"
    return (
        f"<picture>\n"
        f'              <source media="(max-width: 900px)" type="image/webp" srcset="{mob}" />\n'
        f'              <source type="image/webp" srcset="{prefix}{desktop_webp}" />\n'
        f"              {img_tag}\n"
        f"            </picture>"
    )


def strip_responsive_attrs(attrs: str) -> str:
    attrs = re.sub(r'\s+srcset="[^"]*"', "", attrs)
    attrs = re.sub(r'\s+sizes="[^"]*"', "", attrs)
    attrs = re.sub(r'\s+data-full-src="[^"]*"', "", attrs)
    return attrs.rstrip().rstrip("/").rstrip()


def patch_html() -> None:
    updated = 0
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        if path.name.startswith("preview"):
            continue
        text = path.read_text(encoding="utf-8")
        orig = text
        prefix_root = "../assets/imgs/" if path.parent.name == "hu" else "assets/imgs/"

        # --- Hero figure picture ---
        text = re.sub(
            r"<picture>\s*<source[^>]*Hero_img[^>]*>\s*<img([\s\S]*?)/?>\s*</picture>",
            lambda m: picture_mobile_desktop(
                prefix_root,
                mobile_1x="Hero_img-800.webp",
                mobile_2x="Hero_img-1200.webp",
                desktop_webp="Hero_img.webp",
                img_tag=f"<img{strip_responsive_attrs(m.group(1))} />",
            ),
            text,
            flags=re.I,
        )

        # --- Hero background: picture or bare img ---
        def hero_bg_picture(prefix: str, img_attrs: str) -> str:
            attrs = strip_responsive_attrs(img_attrs)
            # ensure png/jpg fallback src if webp was sole src
            if re.search(r'src="[^"]*Hero_background_img\.webp"', attrs):
                attrs = re.sub(
                    r'src="[^"]*Hero_background_img\.webp"',
                    f'src="{prefix}Hero_background_img.png"',
                    attrs,
                )
            return (
                f"<picture>"
                f'<source media="(max-width: 900px)" type="image/webp" '
                f'srcset="{prefix}Hero_background_img-900.webp 1x, {prefix}Hero_background_img-1400.webp 2x" />'
                f'<source type="image/webp" srcset="{prefix}Hero_background_img.webp" />'
                f"<img{attrs} />"
                f"</picture>"
            )

        text = re.sub(
            r"<picture>\s*<source[^>]*Hero_background_img[^>]*>\s*<img([^>]*)/?>\s*</picture>",
            lambda m: hero_bg_picture(prefix_root, m.group(1)),
            text,
            flags=re.I,
        )
        text = re.sub(
            r"<img([^>]*src=\"[^\"]*Hero_background_img\.webp\"[^>]*)/?>",
            lambda m: hero_bg_picture(prefix_root, m.group(1)),
            text,
            flags=re.I,
        )

        # --- Main_Rolam / why-me portrait ---
        def portrait_sub(m: re.Match[str], file_stem: str) -> str:
            attrs = strip_responsive_attrs(m.group(1))
            # keep jpg/png as src
            img = f"<img{attrs} />"
            # data-full-src for lightbox if ever used
            if "data-full-src" not in img:
                img = img.replace(" />", f' data-full-src="{prefix_root}{file_stem}.webp" />')
            return picture_mobile_desktop(
                prefix_root,
                mobile_1x=f"{file_stem}-600.webp",
                mobile_2x=f"{file_stem}-900.webp",
                desktop_webp=f"{file_stem}.webp",
                img_tag=img,
            )

        text = re.sub(
            r"<img([^>]*src=\"[^\"]*Main_Rolam\.jpg\"[^>]*)/?>",
            lambda m: portrait_sub(m, "Main_Rolam"),
            text,
            flags=re.I,
        )
        # If already wrapped badly with srcset on same img, strip first via above

        # Rolam_main.jpg (rólam page) — only if mobile variants exist
        if (IMGS / "Rolam_main-600.webp").exists():
            text = re.sub(
                r"<img([^>]*src=\"[^\"]*Rolam_main\.jpg\"[^>]*)/?>",
                lambda m: portrait_sub(m, "Rolam_main"),
                text,
                flags=re.I,
            )

        # --- Rólam masonry gallery cells ---
        def rolam_gal_sub(m: re.Match[str]) -> str:
            attrs, jpg = m.group(1), m.group(2)
            attrs = strip_responsive_attrs(attrs)
            # path prefix from jpg
            stem = jpg[:-4]
            webp = stem + ".webp"
            w640 = stem + "-640.webp"
            # relative prefix already in jpg path
            return (
                f"<picture>\n"
                f'              <source media="(max-width: 900px)" type="image/webp" srcset="{w640}" />\n'
                f'              <source type="image/webp" srcset="{webp}" />\n'
                f'              <img{attrs} data-full-src="{webp}" />\n'
                f"            </picture>"
            )

        text = re.sub(
            r"<img([^>]*src=\"([^\"]*page-gallery/rolam/[^\"]+\.jpg)\"[^>]*)/?>",
            rolam_gal_sub,
            text,
            flags=re.I,
        )

        # Preload: desktop-quality default href = full webp; keep imagesrcset for mobile LCP
        text = re.sub(
            r'<link rel="preload" as="image" type="image/webp"[^>]*Hero_img[^>]*/?>',
            (
                f'<link rel="preload" as="image" type="image/webp" href="{prefix_root}Hero_img.webp" '
                f'imagesrcset="{prefix_root}Hero_img-800.webp 800w, {prefix_root}Hero_img-1200.webp 1200w, {prefix_root}Hero_img.webp 1536w" '
                f'imagesizes="(max-width: 900px) 100vw, 50vw" fetchpriority="high" />'
            ),
            text,
            count=1,
            flags=re.I,
        )

        if text != orig:
            path.write_text(text, encoding="utf-8")
            updated += 1
            print("html", path.relative_to(ROOT))
    print("html updated", updated)


def main() -> None:
    regenerate_masters()
    patch_html()


if __name__ == "__main__":
    main()
