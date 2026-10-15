# -*- coding: utf-8 -*-
"""Generate WebP derivatives and point HTML imgs at them. Run from repo root."""
from __future__ import annotations

import io
import re
from pathlib import Path

from PIL import Image

ROOT = Path("assets/imgs")


def save_jpeg(im: Image.Image, path: Path, quality: int = 85, max_edge: int = 1600) -> int:
    im = im.convert("RGB")
    w, h = im.size
    scale = min(1.0, max_edge / max(w, h))
    if scale < 1:
        im = im.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    path.write_bytes(buf.getvalue())
    return len(buf.getvalue())


def save_webp(im: Image.Image, path: Path, quality: int = 82, max_edge: int = 1600) -> int:
    im = im.convert("RGB")
    w, h = im.size
    scale = min(1.0, max_edge / max(w, h))
    if scale < 1:
        im = im.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=quality, method=6)
    path.write_bytes(buf.getvalue())
    return len(buf.getvalue())


def edge_for(path: Path) -> int:
    name = path.name
    if any(x in name for x in ("Hero", "Main_", "Kapcsolat", "Rolam", "Szolg", "Manikur", "Szemoldok", "manikur")):
        return 1600
    return 1400


def ensure_from_png() -> None:
    for png_name, quality in (
        ("Hero_img.png", 88),
        ("Hero_background_img.png", 82),
        ("manikur_3.PNG", 88),
    ):
        src = ROOT / png_name
        if not src.exists():
            print("missing", png_name)
            continue
        im = Image.open(src)
        jpg = ROOT / f"{src.stem}.jpg"
        webp = ROOT / f"{src.stem}.webp"
        jb = save_jpeg(im, jpg, quality=quality, max_edge=1600)
        wb = save_webp(im, webp, quality=min(quality, 84), max_edge=1600)
        print(f"PNG {png_name}: JPG {jb/1024:.0f}KB, WEBP {wb/1024:.0f}KB")


def build_webps() -> None:
    for p in sorted(ROOT.rglob("*")):
        if p.suffix.lower() not in {".jpg", ".jpeg"}:
            continue
        if p.name.startswith("og-share"):
            continue
        edge = edge_for(p)
        im = Image.open(p)
        before = p.stat().st_size
        w, h = im.size
        if max(w, h) > edge or before > 250 * 1024:
            # Write candidate to memory; only replace if smaller
            tmp = p.with_suffix(".tmp.jpg")
            buf_size = save_jpeg(im, tmp, quality=85, max_edge=edge)
            if buf_size < before * 0.95:
                tmp.replace(p)
                print(f"shrink {p.relative_to(ROOT)} {before/1024:.0f}->{buf_size/1024:.0f}KB")
                im = Image.open(p)
            else:
                tmp.unlink(missing_ok=True)
        wb = save_webp(im, p.with_suffix(".webp"), quality=82, max_edge=edge)
        print(f"webp {p.relative_to(ROOT)} -> {wb/1024:.0f}KB")


SRC_ATTR = re.compile(
    r"""\b(src)=(["'])([^"']+\.(?:png|PNG|jpg|JPG|jpeg|JPEG))\2"""
)


def update_html() -> None:
    html_files = list(Path(".").glob("*.html")) + list(Path("hu").glob("*.html"))
    changed = 0
    reps = 0

    for hf in html_files:
        text = hf.read_text(encoding="utf-8")

        def repl(m: re.Match[str]) -> str:
            nonlocal reps
            attr, quote, url = m.group(1), m.group(2), m.group(3)
            if url.startswith("http"):
                return m.group(0)
            local = (hf.parent / url).resolve()
            webp = local.with_suffix(".webp")
            if not webp.exists():
                # Hero_img.png -> Hero_img.webp (same stem)
                webp = local.with_name(local.stem + ".webp")
            if webp.exists():
                new_url = url.rsplit(".", 1)[0] + ".webp"
                reps += 1
                return f"{attr}={quote}{new_url}{quote}"
            if local.suffix.lower() == ".png":
                jpg = local.with_name(local.stem + ".jpg")
                if jpg.exists():
                    new_url = url.rsplit(".", 1)[0] + ".jpg"
                    reps += 1
                    return f"{attr}={quote}{new_url}{quote}"
            return m.group(0)

        new = SRC_ATTR.sub(repl, text)
        if new != text:
            hf.write_text(new, encoding="utf-8")
            changed += 1

    print(f"HTML updated: {changed} files, {reps} src swaps")


def main() -> None:
    ensure_from_png()
    build_webps()
    update_html()


if __name__ == "__main__":
    main()
