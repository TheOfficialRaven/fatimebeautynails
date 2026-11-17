# -*- coding: utf-8 -*-
"""
Generate sharp responsive WebP variants + wire srcset/sizes in HTML.
Desktop keeps large candidates; mobile gets smaller widths (not lower quality at same px).
"""
from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent
IMGS = ROOT / "assets" / "imgs"


def resize_width(im: Image.Image, width: int) -> Image.Image:
    w, h = im.size
    if w <= width:
        return im
    nh = max(1, int(round(h * (width / w))))
    out = im.resize((width, nh), Image.Resampling.LANCZOS)
    if out.mode in ("RGB", "RGBA"):
        out = out.filter(ImageFilter.UnsharpMask(radius=0.9, percent=55, threshold=2))
    return out


def resize_max_side(im: Image.Image, max_side: int) -> Image.Image:
    w, h = im.size
    m = max(w, h)
    if m <= max_side:
        return im
    scale = max_side / m
    out = im.resize(
        (max(1, int(round(w * scale))), max(1, int(round(h * scale)))),
        Image.Resampling.LANCZOS,
    )
    if out.mode in ("RGB", "RGBA"):
        out = out.filter(ImageFilter.UnsharpMask(radius=0.9, percent=55, threshold=2))
    return out


def to_rgb_or_rgba(im: Image.Image, keep_alpha: bool) -> Image.Image:
    if keep_alpha:
        return im.convert("RGBA")
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        rgba = im.convert("RGBA")
        bg = Image.new("RGB", rgba.size, (250, 249, 247))
        bg.paste(rgba, mask=rgba.split()[-1])
        return bg
    return im.convert("RGB")


def save_webp(im: Image.Image, dest: Path, quality: int) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=quality, method=6)


def export_widths(
    src: Path,
    *,
    widths: list[int],
    quality: int,
    keep_alpha: bool,
    stem_suffixes: bool = True,
) -> list[tuple[Path, int]]:
    """Return list of (path, width). Largest width uses original stem.webp name if stem_suffixes."""
    base = Image.open(src)
    base = to_rgb_or_rgba(base, keep_alpha)
    outs: list[tuple[Path, int]] = []
    widths_sorted = sorted(set(widths))
    for i, width in enumerate(widths_sorted):
        im = resize_width(base, width)
        if stem_suffixes and i < len(widths_sorted) - 1:
            dest = src.with_name(f"{src.stem}-{im.size[0]}.webp")
        else:
            # largest / primary webp next to source
            dest = src.with_suffix(".webp") if src.suffix.lower() != ".webp" else src
            if src.suffix.lower() == ".webp" and i == len(widths_sorted) - 1:
                dest = src  # overwrite master webp only if regenerating from png
        # If source is already webp and we're writing variants, never overwrite with small
        if src.suffix.lower() == ".webp":
            dest = src.with_name(f"{src.stem}-{im.size[0]}.webp")
            if i == len(widths_sorted) - 1 and im.size[0] >= src.stat().st_size:
                pass
        save_webp(im, dest, quality)
        outs.append((dest, im.size[0]))
        print(f"  {dest.relative_to(IMGS)} {im.size} {dest.stat().st_size/1024:.1f}KB q={quality}")
    return outs


def export_hero_from_png(png: Path, widths: list[int], quality: int) -> None:
    print("HERO", png.name)
    base = to_rgb_or_rgba(Image.open(png), keep_alpha=True)
    for i, width in enumerate(sorted(widths)):
        im = resize_width(base, width)
        if i == len(widths) - 1:
            dest = png.with_suffix(".webp")
        else:
            dest = png.with_name(f"{png.stem}-{im.size[0]}.webp")
        save_webp(im, dest, quality)
        print(f"  {dest.name} {im.size} {dest.stat().st_size/1024:.1f}KB")


def export_gallery_jpg(jpg: Path) -> None:
    base = to_rgb_or_rgba(Image.open(jpg), keep_alpha=False)
    # 640 for mobile grid/carousel @2x; 1200 for lightbox/desktop
    variants = [(640, 85), (1200, 87)]
    for max_side, q in variants:
        im = resize_max_side(base, max_side)
        if max_side == 1200:
            dest = jpg.with_suffix(".webp")
        else:
            dest = jpg.with_name(f"{jpg.stem}-640.webp")
        # skip writing tiny upscales
        if im.size[0] == base.size[0] and im.size[1] == base.size[1] and max_side != 1200:
            # source already smaller than 640 — still write -640 name as copy of full webp later
            pass
        save_webp(im, dest, q)


def export_logo(png: Path) -> None:
    base = to_rgb_or_rgba(Image.open(png), keep_alpha=True)
    # ~90px CSS → 180–200 for retina
    im = resize_width(base, min(200, base.size[0]))
    dest = png.with_suffix(".webp")
    save_webp(im, dest, 90)
    print(f"logo {dest.name} {im.size} {dest.stat().st_size/1024:.1f}KB")


def generate_assets() -> None:
    # Heroes from PNG masters (sharp, high q)
    if (IMGS / "Hero_img.png").exists():
        export_hero_from_png(IMGS / "Hero_img.png", [800, 1200, 1536], quality=90)
    if (IMGS / "Hero_background_img.png").exists():
        export_hero_from_png(IMGS / "Hero_background_img.png", [900, 1400, 2000], quality=88)

    # Main portrait
    rolam = IMGS / "Main_Rolam.jpg"
    if rolam.exists():
        print("Main_Rolam")
        base = to_rgb_or_rgba(Image.open(rolam), False)
        for width, q, name in [
            (600, 86, "Main_Rolam-600.webp"),
            (900, 87, "Main_Rolam-900.webp"),
            (1200, 88, "Main_Rolam.webp"),
        ]:
            im = resize_width(base, width)
            dest = IMGS / name
            save_webp(im, dest, q)
            print(f"  {name} {im.size} {dest.stat().st_size/1024:.1f}KB")

    # Gallery JPGs
    gallery = list((IMGS / "page-gallery").rglob("*.jpg"))
    print("gallery", len(gallery))
    for i, jpg in enumerate(gallery, 1):
        export_gallery_jpg(jpg)
        if i % 15 == 0:
            print(f"  … {i}/{len(gallery)}")

    # Logos
    for png in sorted((IMGS / "Logo_Carousel").glob("*.png")):
        export_logo(png)


def srcset_webp(prefix: str, stem_path: str, widths_files: list[tuple[str, int]]) -> str:
    """widths_files: list of (filename, w)"""
    return ", ".join(f"{prefix}{fn} {w}w" for fn, w in widths_files)


def patch_html() -> None:
    # Heroes
    hero_figure_re = re.compile(
        r"<picture>\s*<source type=\"image/webp\" srcset=\"([^\"]*Hero_img\.webp)\"\s*/>\s*"
        r"<img(\s+class=\"hero__image-figure\"[\s\S]*?)/?>\s*</picture>",
        re.I,
    )
    hero_bg_re = re.compile(
        r"<picture>\s*<source type=\"image/webp\" srcset=\"([^\"]*Hero_background_img\.webp)\"\s*/>\s*"
        r"<img([^>]*)/?>\s*</picture>",
        re.I,
    )
    # Bare hero bg webp img (some pages)
    hero_bg_img_re = re.compile(
        r"<img([^>]*src=\"([^\"]*Hero_background_img\.webp)\"[^>]*)/?>",
        re.I,
    )

    gallery_img_re = re.compile(
        r"<img([^>]*src=\"([^\"]*page-gallery/[^\"]+\.jpg)\"[^>]*)/?>",
        re.I,
    )

    main_rolam_re = re.compile(
        r"<img([^>]*src=\"([^\"]*Main_Rolam\.jpg)\"[^>]*)/?>",
        re.I,
    )

    logo_re = re.compile(
        r"<img([^>]*class=\"partners__logo\"[^>]*src=\"([^\"]*Logo_Carousel/[^\"]+\.png)\"[^>]*)/?>|"
        r"<img([^>]*src=\"([^\"]*Logo_Carousel/[^\"]+\.png)\"[^>]*class=\"partners__logo\"[^>]*)/?>",
        re.I,
    )

    preload_hero_re = re.compile(
        r'<link rel="preload" as="image" type="image/webp" href="([^"]*Hero_img\.webp)"([^>]*)/?>',
        re.I,
    )

    updated = 0
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        if path.name.startswith("preview"):
            continue
        text = path.read_text(encoding="utf-8")
        orig = text

        def hero_figure_sub(m: re.Match[str]) -> str:
            webp = m.group(1)
            img_attrs = m.group(2)
            prefix = webp.rsplit("/", 1)[0] + "/"
            # derive sibling names
            w800 = prefix + "Hero_img-800.webp"
            w1200 = prefix + "Hero_img-1200.webp"
            srcset = f"{w800} 800w, {w1200} 1200w, {webp} 1536w"
            sizes = "(max-width: 900px) 100vw, min(52vw, 780px)"
            return (
                f'<picture>\n'
                f'              <source type="image/webp" srcset="{srcset}" sizes="{sizes}" />\n'
                f'              <img{img_attrs}/>\n'
                f'            </picture>'
            )

        text = hero_figure_re.sub(hero_figure_sub, text)

        def hero_bg_pic_sub(m: re.Match[str]) -> str:
            webp = m.group(1)
            img_attrs = m.group(2)
            prefix = webp.rsplit("/", 1)[0] + "/"
            srcset = (
                f"{prefix}Hero_background_img-900.webp 900w, "
                f"{prefix}Hero_background_img-1400.webp 1400w, "
                f"{webp} 2000w"
            )
            sizes = "100vw"
            return (
                f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}" />'
                f"<img{img_attrs}/></picture>"
            )

        text = hero_bg_re.sub(hero_bg_pic_sub, text)

        def hero_bg_img_sub(m: re.Match[str]) -> str:
            attrs, webp = m.group(1), m.group(2)
            if "srcset=" in attrs:
                return m.group(0)
            prefix = webp.rsplit("/", 1)[0] + "/"
            srcset = (
                f"{prefix}Hero_background_img-900.webp 900w, "
                f"{prefix}Hero_background_img-1400.webp 1400w, "
                f"{webp} 2000w"
            )
            # inject srcset/sizes into img
            if "sizes=" not in attrs:
                attrs = attrs + f' srcset="{srcset}" sizes="100vw"'
            else:
                attrs = attrs + f' srcset="{srcset}"'
            return f"<img{attrs}/>"

        text = hero_bg_img_re.sub(hero_bg_img_sub, text)

        def gallery_sub(m: re.Match[str]) -> str:
            attrs, jpg = m.group(1), m.group(2)
            attrs = attrs.rstrip().rstrip("/").rstrip()
            if "srcset=" in attrs or "data-full-src=" in attrs:
                return m.group(0)
            stem = jpg[:-4]
            webp = stem + ".webp"
            w640 = stem + "-640.webp"
            srcset = f"{w640} 640w, {webp} 1200w"
            sizes = "(max-width: 900px) 45vw, 280px"
            if "page-gallery__img" in attrs:
                sizes = "(max-width: 900px) 90vw, 280px"
            if "/rolam/" in jpg.replace("\\", "/"):
                sizes = "(max-width: 900px) 50vw, min(42vw, 520px)"
            return (
                f'<img{attrs} srcset="{srcset}" sizes="{sizes}" '
                f'data-full-src="{webp}" />'
            )

        text = gallery_img_re.sub(gallery_sub, text)

        def rolam_sub(m: re.Match[str]) -> str:
            attrs, jpg = m.group(1), m.group(2)
            if "srcset=" in attrs:
                return m.group(0)
            prefix = jpg.rsplit("/", 1)[0] + "/"
            srcset = (
                f"{prefix}Main_Rolam-600.webp 600w, "
                f"{prefix}Main_Rolam-900.webp 900w, "
                f"{prefix}Main_Rolam.webp 1200w"
            )
            sizes = "(max-width: 900px) 92vw, min(36vw, 420px)"
            return (
                f"<img{attrs} srcset=\"{srcset}\" sizes=\"{sizes}\" "
                f'data-full-src="{prefix}Main_Rolam.webp"/>'
            )

        text = main_rolam_re.sub(rolam_sub, text)

        def logo_sub(m: re.Match[str]) -> str:
            if m.group(1) is not None:
                attrs, png = m.group(1), m.group(2)
            else:
                attrs, png = m.group(3), m.group(4)
            webp = png[:-4] + ".webp"
            # swap png → webp src (small logos, sharp enough)
            attrs2 = attrs.replace(png, webp)
            return f"<img{attrs2}/>"

        text = logo_re.sub(logo_sub, text)

        def preload_sub(m: re.Match[str]) -> str:
            href, rest = m.group(1), m.group(2)
            prefix = href.rsplit("/", 1)[0] + "/"
            imagesrcset = (
                f"{prefix}Hero_img-800.webp 800w, "
                f"{prefix}Hero_img-1200.webp 1200w, "
                f"{href} 1536w"
            )
            imagesizes = "(max-width: 900px) 100vw, min(52vw, 780px)"
            return (
                f'<link rel="preload" as="image" type="image/webp" href="{prefix}Hero_img-800.webp" '
                f'imagesrcset="{imagesrcset}" imagesizes="{imagesizes}"{rest}/>'
            )

        text = preload_hero_re.sub(preload_sub, text)

        if text != orig:
            path.write_text(text, encoding="utf-8")
            updated += 1
            print("html", path.relative_to(ROOT))
    print("html updated", updated)


def main() -> None:
    generate_assets()
    patch_html()


if __name__ == "__main__":
    main()
