# -*- coding: utf-8 -*-
"""Ensure styles-pages.min.css is linked on subpages (blocking, after core)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SKIP_NAMES = {
    "index.html",
    "preview-og.html",
    "preview-salon-email.html",
}

PAGES_LINK_RE = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)?css/styles-pages\.min\.css"\s*/?>\s*',
    re.I,
)

CORE_READY_RE = re.compile(
    r'([ \t]*<link rel="stylesheet" href="((?:\.\./)?css/styles\.min\.css)"\s*/?>\s*)'
    r'(?:[ \t]*<link rel="stylesheet" href="(?:\.\./)?css/styles-pages\.min\.css"\s*/?>\s*)?'
    r'([ \t]*<script>document\.documentElement\.classList\.add\(["\']css-ready["\']\);?</script>\s*)?',
    re.I,
)


def is_redirect(text: str) -> bool:
    return 'http-equiv="refresh"' in text or "window.location.replace" in text


def fix_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if path.name in SKIP_NAMES or is_redirect(text):
        if PAGES_LINK_RE.search(text):
            path.write_text(PAGES_LINK_RE.sub("", text), encoding="utf-8")
            return "removed-from-home"
        return "skip"

    if "css/styles.min.css" not in text:
        return "skip-no-css"

    prefix = "../" if path.parent.name == "hu" else ""
    pages = f'{prefix}css/styles-pages.min.css'

    m = CORE_READY_RE.search(text)
    if not m:
        return "no-core-css"

    core_href = m.group(2)
    block = (
        f'  <link rel="stylesheet" href="{core_href}" />\n'
        f'  <link rel="stylesheet" href="{pages}" />\n'
        f'  <script>document.documentElement.classList.add("css-ready");</script>\n'
    )
    new = CORE_READY_RE.sub(block, text, count=1)
    if new != text:
        path.write_text(new, encoding="utf-8")
        return "updated"
    return "unchanged"


def main() -> None:
    counts: dict[str, int] = {}
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        status = fix_file(path)
        counts[status] = counts.get(status, 0) + 1
        if status.startswith("updated") or status in {"removed-from-home", "no-core-css"}:
            print(status, path.relative_to(ROOT))
    print("summary", counts)


if __name__ == "__main__":
    main()
