# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Broken: ...1200w sizes=  (missing " after 1200w)
BROKEN = re.compile(
    r'(srcset="(?:\.\./)?assets/imgs/page-gallery/[^"\s]+-400\.webp 400w, '
    r'(?:\.\./)?assets/imgs/page-gallery/[^"\s]+-640\.webp 640w, '
    r'(?:\.\./)?assets/imgs/page-gallery/[^"\s]+\.webp 1200w)(\s+sizes=)'
)


def main() -> None:
    n = 0
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        text = path.read_text(encoding="utf-8")
        new = BROKEN.sub(r'\1"\2', text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            n += 1
            print("fixed", path.relative_to(ROOT))
    print("total", n)
    sample = (ROOT / "index.html").read_text(encoding="utf-8")
    m = re.search(r'srcset="[^"]*szempilla-02[^"]*"', sample)
    print(m.group(0) if m else "NO MATCH")


if __name__ == "__main__":
    main()
