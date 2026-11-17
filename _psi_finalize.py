# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def minify_css(src: str) -> str:
    out = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    out = re.sub(r"\s+", " ", out)
    out = re.sub(r"\s*([{}:;,>])\s*", r"\1", out)
    return out.replace(";}", "}").strip()


def minify_js(src: str) -> str:
    out = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    out = re.sub(r"(?m)^\s*//.*$", "", out)
    out = re.sub(r"\n\s*\n", "\n", out)
    return out


def main() -> None:
    (ROOT / "css" / "styles.min.css").write_text(
        minify_css((ROOT / "css" / "styles.css").read_text(encoding="utf-8")),
        encoding="utf-8",
    )
    pages_src = ROOT / "css" / "styles-pages.css"
    if pages_src.exists():
        (ROOT / "css" / "styles-pages.min.css").write_text(
            minify_css(pages_src.read_text(encoding="utf-8")),
            encoding="utf-8",
        )
    (ROOT / "js" / "main.min.js").write_text(
        minify_js((ROOT / "js" / "main.js").read_text(encoding="utf-8")),
        encoding="utf-8",
    )

    updated = 0
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        text = path.read_text(encoding="utf-8")
        new = text
        new = re.sub(
            r'<script src="([^"]*main\.min\.js)"></script>',
            r'<script src="\1" defer></script>',
            new,
        )
        new = re.sub(
            r'<script src="([^"]*lang-transition-init\.js)"></script>',
            r'<script src="\1" defer></script>',
            new,
        )
        new = new.replace('width="1200" height="1400"', 'width="1200" height="800"')
        if new != text:
            path.write_text(new, encoding="utf-8")
            updated += 1

    print("html updated", updated)
    print("styles.min KB", round((ROOT / "css" / "styles.min.css").stat().st_size / 1024, 1))
    pages_min = ROOT / "css" / "styles-pages.min.css"
    if pages_min.exists():
        print("styles-pages.min KB", round(pages_min.stat().st_size / 1024, 1))
    print("main.min KB", round((ROOT / "js" / "main.min.js").stat().st_size / 1024, 1))
    print("gold token", "#8a7644" in (ROOT / "css" / "styles.min.css").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
