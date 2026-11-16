# -*- coding: utf-8 -*-
"""Generate optimized WebP assets for PageSpeed (does not delete originals)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
IMGS = ROOT / "assets" / "imgs"


def save_webp(
    src: Path,
    dest: Path,
    max_side: int | None = 1400,
    quality: int = 88,
    *,
    keep_alpha: bool = False,
) -> None:
    im = Image.open(src)
    has_alpha = keep_alpha and (
        im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    )
    if has_alpha:
        im = im.convert("RGBA")
    else:
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
        # Flatten alpha onto off-white unless transparency must be kept
        if im.mode == "RGBA":
            bg = Image.new("RGB", im.size, (250, 249, 247))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")
    w, h = im.size
    if max_side:
        scale = min(1.0, max_side / max(w, h))
        if scale < 1:
            im = im.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=quality, method=6)
    print(
        f"{src.name}: {src.stat().st_size/1024:.0f}KB -> {dest.name} "
        f"{dest.stat().st_size/1024:.0f}KB {im.size} {im.mode}"
    )


def main() -> None:
    # Hero LCP / background — figure + bg must keep transparency
    save_webp(
        IMGS / "Hero_img.png",
        IMGS / "Hero_img.webp",
        max_side=1536,
        quality=90,
        keep_alpha=True,
    )
    save_webp(
        IMGS / "Hero_background_img.png",
        IMGS / "Hero_background_img.webp",
        max_side=2000,
        quality=88,
        keep_alpha=True,
    )

    # About / home media often listed by PSI
    for name, side, q in [
        ("Main_Rolam.webp", 1000, 75),
        ("Main_Rolam.jpg", 1000, 75),
    ]:
        src = IMGS / name
        if src.exists() and src.suffix.lower() != ".webp":
            save_webp(src, IMGS / (src.stem + ".webp"), side, q)
        elif src.exists() and src.suffix.lower() == ".webp" and src.stat().st_size > 80_000:
            # recompress oversized webp in place via temp
            tmp = src.with_suffix(".tmp.webp")
            save_webp(src, tmp, side, q)
            if tmp.stat().st_size < src.stat().st_size:
                src.write_bytes(tmp.read_bytes())
                print(f"  replaced {src.name}")
            tmp.unlink(missing_ok=True)

    # Logo carousel → webp (alpha preserved)
    logo_dir = IMGS / "Logo_Carousel"
    for src in sorted(logo_dir.glob("*.png")):
        save_webp(
            src,
            logo_dir / (src.stem + ".webp"),
            max_side=None,
            quality=95,
            keep_alpha=True,
        )

    # Page gallery: rebuild from originals when present (sharper, less downscale)
    gal = IMGS / "page-gallery"
    for webp in sorted(gal.rglob("*.webp")):
        src = None
        for ext in (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"):
            cand = webp.with_suffix(ext)
            if cand.exists():
                src = cand
                break
        if not src:
            continue
        save_webp(
            src,
            webp,
            max_side=1400,
            quality=88,
            keep_alpha=src.suffix.lower() == ".png",
        )


if __name__ == "__main__":
    main()
