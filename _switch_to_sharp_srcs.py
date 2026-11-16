# -*- coding: utf-8 -*-
"""Point HTML image refs to original sharp JPG/PNG; regenerate high-quality transparent WebPs."""
from __future__ import annotations

import re
import time
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent
IMGS = ROOT / "assets" / "imgs"


def atomic_save_webp(im: Image.Image, dest: Path, **kwargs) -> None:
    tmp = dest.with_suffix(".tmp.webp")
    im.save(tmp, "WEBP", **kwargs)
    for _ in range(8):
        try:
            if dest.exists():
                dest.unlink()
            tmp.replace(dest)
            return
        except OSError:
            time.sleep(0.35)
    dest.write_bytes(tmp.read_bytes())
    tmp.unlink(missing_ok=True)


def remake_transparent_heros() -> None:
    # Near-max quality, full resolution, mild sharpen
    for name, q in (("Hero_img.png", 95), ("Hero_background_img.png", 92)):
        src = IMGS / name
        im = Image.open(src).convert("RGBA")
        im = im.filter(ImageFilter.UnsharpMask(radius=0.8, percent=55, threshold=2))
        dest = IMGS / f"{src.stem}.webp"
        atomic_save_webp(im, dest, quality=q, method=6)
        print(f"{dest.name}: {im.size} {im.mode} {dest.stat().st_size/1024:.0f}KB")


def prefer_original_in_html(text: str) -> str:
    # Gallery webp -> jpg
    text = re.sub(
        r"(assets/imgs/page-gallery/[^\"']+?)\.webp",
        r"\1.jpg",
        text,
    )
    # Logo carousel webp -> png
    text = re.sub(
        r"(assets/imgs/Logo_Carousel/[^\"']+?)\.webp",
        r"\1.png",
        text,
    )
    # Main_* content photos
    for stem in (
        "Main_Rolam",
        "Main_kapcsolat",
        "Main_callux",
        "Szolg_main",
        "Szolg_1",
        "Szolg_2",
        "Szolg_3",
        "popup_img",
    ):
        jpg = IMGS / f"{stem}.jpg"
        png = IMGS / f"{stem}.png"
        if jpg.exists():
            text = text.replace(f"assets/imgs/{stem}.webp", f"assets/imgs/{stem}.jpg")
        elif png.exists() and stem == "popup_img":
            # keep webp for popup if we want size — user wants sharp: use png
            text = text.replace(f"assets/imgs/{stem}.webp", f"assets/imgs/{stem}.png")
    # Also fix JS popup path back to png for sharpness+alpha
    return text


def fix_js_popup() -> None:
    main = ROOT / "js" / "main.js"
    t = main.read_text(encoding="utf-8")
    n = t.replace("popup_img.webp", "popup_img.png")
    if n != t:
        main.write_text(n, encoding="utf-8")
        print("main.js popup -> png")
    # refresh min
    import re as _re

    j = _re.sub(r"/\*.*?\*/", "", n, flags=_re.S)
    j = _re.sub(r"(?m)^\s*//.*$", "", j)
    j = _re.sub(r"\n\s*\n", "\n", j)
    (ROOT / "js" / "main.min.js").write_text(j, encoding="utf-8")


def main() -> None:
    remake_transparent_heros()
    updated = 0
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        text = path.read_text(encoding="utf-8")
        new = prefer_original_in_html(text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            updated += 1
            print("html", path.relative_to(ROOT))
    fix_js_popup()
    print("html files updated", updated)


if __name__ == "__main__":
    main()
