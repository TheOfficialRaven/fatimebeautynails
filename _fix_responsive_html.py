# -*- coding: utf-8 -*-
"""Repair broken self-closing img/link tags after responsive image patch."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text

    # 1) link ... //>  →  />
    text = re.sub(r"(<link\b[^>]*?)\s*//>", r"\1 />", text, flags=re.I)

    # 2) img ... //> or ... //></picture>
    text = re.sub(r"(<img\b[^>]*?)\s*//>", r"\1 />", text, flags=re.I)

    # 3) Attributes accidentally placed after a premature /
    #    loading="lazy"\n            / srcset="..." sizes="..." data-full-src="..."/>
    text = re.sub(
        r"(<img\b[\s\S]*?)\s*/\s+(srcset=\"[^\"]*\"\s+sizes=\"[^\"]*\"(?:\s+data-full-src=\"[^\"]*\")?)\s*/?>",
        r"\1 \2 />",
        text,
        flags=re.I,
    )

    # 4) Same for single-line: ... / srcset="..." />
    text = re.sub(
        r"(<img\b[^>]*?)\s*/\s+(srcset=\"[^\"]*\"\s+sizes=\"[^\"]*\"(?:\s+data-full-src=\"[^\"]*\")?)\s*/?>",
        r"\1 \2 />",
        text,
        flags=re.I,
    )

    # 5) Collapse duplicate spaces before />
    text = re.sub(r"\s+/>", " />", text)

    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    n = 0
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        if path.name.startswith("preview"):
            continue
        if fix_file(path):
            n += 1
            print("fixed", path.relative_to(ROOT))
    print("done", n)


if __name__ == "__main__":
    main()
