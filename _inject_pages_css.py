# -*- coding: utf-8 -*-
"""Inject deferred styles-pages.min.css on subpages (not homepage / redirects)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SKIP_NAMES = {
    "index.html",
    "preview-og.html",
    "preview-salon-email.html",
}

PAGES_BLOCK_RE = re.compile(
    r"[ \t]*<link rel=\"preload\" href=\"((?:\.\./)?css/styles-pages\.min\.css)\" as=\"style\"[\s\S]*?"
    r"(?:<noscript><link rel=\"stylesheet\" href=\"(?:\.\./)?css/styles-pages\.min\.css\"\s*/?></noscript>\s*)?",
    re.I,
)

CORE_BLOCK_END_RE = re.compile(
    r'(<link rel="preload" href="((?:\.\./)?css/styles\.min\.css)" as="style"[^>]*>\s*'
    r'<noscript><link rel="stylesheet" href="(?:\.\./)?css/styles\.min\.css"\s*/?></noscript>\s*'
    r"<script>!function\(d\)\{var l=d\.querySelector\('link\[rel=preload\]\[as=style\]\[href=\"(?:\.\./)?css/styles\.min\.css\"\]'\);.*?</script>\s*)",
    re.S | re.I,
)


def pages_css_block(prefix: str) -> str:
    href = f"{prefix}css/styles-pages.min.css"
    return (
        f'  <link rel="preload" href="{href}" as="style" '
        f'onload="this.onload=null;this.rel=\'stylesheet\'" />\n'
        f'  <noscript><link rel="stylesheet" href="{href}" /></noscript>\n'
    )


def is_redirect(text: str) -> bool:
    return "http-equiv=\"refresh\"" in text or "window.location.replace" in text


def fix_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if path.name in SKIP_NAMES or is_redirect(text):
        # Ensure homepage does not load pages CSS
        if PAGES_BLOCK_RE.search(text):
            text2 = PAGES_BLOCK_RE.sub("", text)
            if text2 != text:
                path.write_text(text2, encoding="utf-8")
                return "removed-from-home"
        return "skip"

    prefix = "../" if path.parent.name == "hu" else ""
    # Remove any existing pages block then re-inject cleanly
    text = PAGES_BLOCK_RE.sub("", text)

    m = CORE_BLOCK_END_RE.search(text)
    if not m:
        return "no-core-css"

    insert = m.group(1) + pages_css_block(prefix)
    text = CORE_BLOCK_END_RE.sub(insert, text, count=1)
    path.write_text(text, encoding="utf-8")
    return "updated"


def main() -> None:
    counts: dict[str, int] = {}
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        status = fix_file(path)
        counts[status] = counts.get(status, 0) + 1
        if status in {"updated", "removed-from-home", "no-core-css"}:
            print(status, path.relative_to(ROOT))
    print("summary", counts)


if __name__ == "__main__":
    main()
