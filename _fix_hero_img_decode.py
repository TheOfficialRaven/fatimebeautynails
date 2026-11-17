# -*- coding: utf-8 -*-
"""Hero LCP images: sync decode to avoid late paint pop/jump."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def fix(text: str) -> str:
    # Background LCP img
    text = re.sub(
        r'(src="(?:\.\./)?assets/imgs/Hero_background_img\.png"[^>]*?)decoding="async"',
        r'\1decoding="sync"',
        text,
    )
    # Foreground figure
    text = re.sub(
        r'(class="hero__image-figure"[^>]*?)decoding="async"',
        r'\1decoding="sync"',
        text,
    )
    # page-hero bg if present
    text = re.sub(
        r'(class="page-hero__image-bg"[\s\S]*?<img[^>]*?)decoding="async"',
        lambda m: m.group(0).replace('decoding="async"', 'decoding="sync"', 1)
        if 'decoding="async"' in m.group(0)
        else m.group(0),
        text,
        count=1,
    )
    return text


def main() -> None:
    n = 0
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        if path.name.startswith("preview"):
            continue
        text = path.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in text:
            continue
        new = fix(text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            n += 1
            print("fixed", path.relative_to(ROOT))
    print("total", n)


if __name__ == "__main__":
    main()
