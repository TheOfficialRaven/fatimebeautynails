# -*- coding: utf-8 -*-
"""Sharper large photos: Rolam mobile 900, true 640w gallery, split-info sizes."""
from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent
IMGS = ROOT / "assets" / "imgs"


def save_webp(src: Path, dest: Path, *, width: int, quality: int = 82) -> None:
    im = Image.open(src)
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        rgba = im.convert("RGBA")
        bg = Image.new("RGB", rgba.size, (250, 249, 247))
        bg.paste(rgba, mask=rgba.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    w, h = im.size
    if w > width:
        nh = max(1, int(round(h * (width / w))))
        im = im.resize((width, nh), Image.Resampling.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=0.9, percent=70, threshold=2))
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=quality, method=6)
    print(f"{dest.relative_to(IMGS)}: {im.size} {dest.stat().st_size/1024:.0f} KiB q{quality}")


def regenerate_assets() -> None:
    # Portrait: sharp 900 for mobile (displayed ~full width)
    save_webp(IMGS / "Main_Rolam.jpg", IMGS / "Main_Rolam-900.webp", width=900, quality=84)
    # Keep 600 as lighter 1x option
    save_webp(IMGS / "Main_Rolam.jpg", IMGS / "Main_Rolam-600.webp", width=600, quality=80)

    # True 640-wide gallery thumbs (many were incorrectly ~480)
    for path in (IMGS / "page-gallery").rglob("*-640.webp"):
        stem = path.name.replace("-640.webp", "")
        full = path.with_name(stem + ".webp")
        jpg = path.with_name(stem + ".jpg")
        src = full if full.exists() else jpg
        if not src.exists():
            print("skip", path)
            continue
        save_webp(src, path, width=640, quality=80)


def patch_html() -> None:
    n = 0
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        text = path.read_text(encoding="utf-8")
        orig = text

        # Rolam: mobile denser — 600 for 1x, 900 for 2x
        text = re.sub(
            r'(media="\(max-width: 900px\)" type="image/webp" srcset=")'
            r'((?:\.\./)?assets/imgs/Main_Rolam)-600\.webp"',
            r'\1\2-600.webp 1x, \2-900.webp 2x"',
            text,
        )
        # Also handle if already only -900
        text = re.sub(
            r'(media="\(max-width: 900px\)" type="image/webp" srcset=")'
            r'((?:\.\./)?assets/imgs/Main_Rolam)-900\.webp"',
            r'\1\2-600.webp 1x, \2-900.webp 2x"',
            text,
        )

        # split-info hero images: large frame, not gallery thumb sizes
        def fix_split_sizes(m: re.Match[str]) -> str:
            block = m.group(0)
            block = re.sub(
                r'sizes="\(max-width: 900px\) 42vw, 280px"',
                'sizes="(max-width: 900px) 92vw, (max-width: 1200px) 46vw, 520px"',
                block,
            )
            # if already some other sizes, force correct for split-info
            if "sizes=" in block and "92vw" not in block:
                block = re.sub(
                    r'sizes="[^"]*"',
                    'sizes="(max-width: 900px) 92vw, (max-width: 1200px) 46vw, 520px"',
                    block,
                    count=1,
                )
            return block

        text = re.sub(
            r'<img\s+class="split-info__img[^"]*"[\s\S]*?>',
            fix_split_sizes,
            text,
        )

        # Home / ref grid thumbs stay 42vw; page-gallery carousel already 90vw — bump desktop a bit
        # Page gallery: desktop slides often ~half container — 280 too small on retina
        text = text.replace(
            'sizes="(max-width: 900px) 90vw, 280px"',
            'sizes="(max-width: 900px) 92vw, (max-width: 1200px) 42vw, 360px"',
        )

        if text != orig:
            path.write_text(text, encoding="utf-8")
            n += 1
            print("html", path.relative_to(ROOT))
    print("html updated", n)


def main() -> None:
    regenerate_assets()
    patch_html()
    # verify piercing-08 and rolam
    for rel in (
        "Main_Rolam-900.webp",
        "Main_Rolam-600.webp",
        "page-gallery/piercing/piercing-08-640.webp",
    ):
        p = IMGS / rel
        im = Image.open(p)
        print("check", rel, im.size, f"{p.stat().st_size/1024:.0f}KiB")


if __name__ == "__main__":
    main()
