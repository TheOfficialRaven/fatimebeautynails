# -*- coding: utf-8 -*-
"""Set partner logo width/height attributes to the real intrinsic sizes (CLS)."""
from __future__ import annotations

import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
LOGOS = ROOT / "assets" / "imgs" / "Logo_Carousel"

IMG_RE = re.compile(
    r'(<img class="partners__logo" src="(?:\.\./)?assets/imgs/Logo_Carousel/([^"]+)"[^>]*?)'
    r'width="\d+" height="\d+"'
)


def main() -> None:
    sizes = {p.name: Image.open(p).size for p in LOGOS.glob("*.webp")}
    n = 0
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        text = path.read_text(encoding="utf-8")
        if "partners__logo" not in text:
            continue

        def repl(m: re.Match[str]) -> str:
            size = sizes.get(m.group(2))
            if not size:
                return m.group(0)
            return f'{m.group(1)}width="{size[0]}" height="{size[1]}"'

        new = IMG_RE.sub(repl, text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            n += 1
            print("fixed", path.relative_to(ROOT))
    print("total", n)


if __name__ == "__main__":
    main()
