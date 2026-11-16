# -*- coding: utf-8 -*-
"""Re-export images: keep alpha where needed, higher quality / less downscale."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent
IMGS = ROOT / "assets" / "imgs"


def resize_max(im: Image.Image, max_side: int | None) -> Image.Image:
    if not max_side:
        return im
    w, h = im.size
    scale = min(1.0, max_side / max(w, h))
    if scale >= 1:
        return im
    return im.resize(
        (max(1, int(w * scale)), max(1, int(h * scale))),
        Image.Resampling.LANCZOS,
    )


def save_webp(
    src: Path,
    dest: Path,
    *,
    max_side: int | None,
    quality: int,
    keep_alpha: bool,
    sharpen: bool = False,
    lossless: bool = False,
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

    im = resize_max(im, max_side)
    if sharpen and im.mode in ("RGB", "RGBA"):
        # mild restore after downscale — logos skip this
        im = im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=70, threshold=2))

    dest.parent.mkdir(parents=True, exist_ok=True)
    if lossless:
        im.save(dest, "WEBP", lossless=True, method=6)
    else:
        im.save(dest, "WEBP", quality=quality, method=6)
    print(
        f"{src.relative_to(IMGS)} -> {dest.name}: "
        f"{src.stat().st_size/1024:.0f}KB -> {dest.stat().st_size/1024:.0f}KB "
        f"{im.size} {im.mode}"
    )


def main() -> None:
    # Home / subpage hero figure + background (transparency)
    save_webp(
        IMGS / "Hero_img.png",
        IMGS / "Hero_img.webp",
        max_side=1536,
        quality=90,
        keep_alpha=True,
        sharpen=True,
    )
    save_webp(
        IMGS / "Hero_background_img.png",
        IMGS / "Hero_background_img.webp",
        max_side=2000,
        quality=88,
        keep_alpha=True,
        sharpen=True,
    )

    # Partner logos — alpha + lossless/high quality, no downscale
    logo_dir = IMGS / "Logo_Carousel"
    for src in sorted(logo_dir.glob("*.png")):
        save_webp(
            src,
            logo_dir / f"{src.stem}.webp",
            max_side=None,
            quality=95,
            keep_alpha=True,
            sharpen=False,
            lossless=True,
        )

    # Popup
    popup = IMGS / "popup_img.png"
    if popup.exists():
        save_webp(
            popup,
            IMGS / "popup_img.webp",
            max_side=1200,
            quality=88,
            keep_alpha=True,
            sharpen=True,
        )

    # About media
    for name in ("Main_Rolam.jpg", "Main_Rolam.png"):
        src = IMGS / name
        if src.exists():
            save_webp(
                src,
                IMGS / "Main_Rolam.webp",
                max_side=1400,
                quality=88,
                keep_alpha=False,
                sharpen=True,
            )
            break

    # Gallery: rebuild from JPG/PNG originals at sharper settings
    gal = IMGS / "page-gallery"
    for webp in sorted(gal.rglob("*.webp")):
        src = None
        for ext in (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"):
            cand = webp.with_suffix(ext)
            if cand.exists():
                src = cand
                break
        if not src:
            print("skip (no source)", webp.relative_to(IMGS))
            continue
        save_webp(
            src,
            webp,
            max_side=1400,
            quality=88,
            keep_alpha=src.suffix.lower() == ".png",
            sharpen=True,
        )


if __name__ == "__main__":
    main()
