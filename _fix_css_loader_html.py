# -*- coding: utf-8 -*-
"""Repair mangled head CSS/fonts blocks that cause section jumps on navigation."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
from _apply_async_css_safe import CRITICAL, css_loader_block

CRITICAL_RE = re.compile(r"/\*critical\*/.*?(?=</style>)", re.S)

# From fonts.googleapis stylesheet / preconnect block end through </head>
HEAD_TAIL_RE = re.compile(
    r"(<link\s+rel=\"preconnect\"\s+href=\"https://fonts\.googleapis\.com\"\s*/>\s*"
    r"<link\s+rel=\"preconnect\"\s+href=\"https://fonts\.gstatic\.com\"\s+crossorigin\s*/>\s*"
    r"<link\s+rel=\"preload\"\s+as=\"style\"\s+href=\"https://fonts\.googleapis\.com[^>]*>\s*"
    r"<link\s+href=\"https://fonts\.googleapis\.com[^>]*rel=\"stylesheet\"[^>]*>\s*)"
    r"[\s\S]*?"
    r"</head>",
    re.I,
)

FONTS_NOSCRIPT = (
    "  <noscript>\n"
    "    <link\n"
    '      href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;500;600;700'
    "&family=Gilda+Display&family=League+Spartan:wght@300;400;500;600;700&display=swap\"\n"
    '      rel="stylesheet" />\n'
    "  </noscript>\n"
)


def is_redirect(text: str) -> bool:
    return 'http-equiv="refresh"' in text or "window.location.replace" in text


def image_preloads(text: str, prefix: str) -> str:
    """Keep home hero image preloads if present."""
    lines = []
    for m in re.finditer(
        r'[ \t]*<link rel="preload" as="image"[^>]*>\s*',
        text,
    ):
        lines.append(m.group(0).rstrip() + "\n")
    return "".join(lines)


def fix_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if is_redirect(text):
        return "redirect"

    if "/*critical*/" in text:
        text = CRITICAL_RE.sub(f"/*critical*/{CRITICAL}", text, count=1)

    prefix = "../" if path.parent.name == "hu" else ""
    core = f"{prefix}css/styles.min.css"
    pages = None if path.name == "index.html" else f"{prefix}css/styles-pages.min.css"

    m = HEAD_TAIL_RE.search(text)
    if not m:
        # Fallback: rewrite from first fonts noscript / css boot to </head>
        m2 = re.search(
            r"(?:[ \t]*<noscript>\s*<link[^>]*fonts\.googleapis\.com[\s\S]*?</noscript>\s*)+"
            r"|(?:[ \t]*<script>\(function\(d\)\{var left=\d+;)",
            text,
            re.I,
        )
        if not m2:
            return "no-tail"
        start = m2.start()
        end = text.find("</head>", start)
        if end < 0:
            return "no-head"
        imgs = image_preloads(text[start:end], prefix)
        new_tail = FONTS_NOSCRIPT + imgs + css_loader_block(core, pages) + "</head>"
        # If fonts noscript already preceded by print stylesheet, keep from start
        # but we may double fonts noscript — trim: start at css boot if fonts already ok
        before = text[:start]
        if "fonts.googleapis.com" in before[-1200:] and "<noscript>" not in before[-400:]:
            # print stylesheet already there; start was fonts noscript — OK
            pass
        text = before + new_tail + text[end + len("</head>") :]
        path.write_text(text, encoding="utf-8")
        return "fixed-fallback"

    fonts_links = m.group(1)
    # Normalize whitespace on captured fonts links block
    imgs = image_preloads(m.group(0), prefix)
    new_block = (
        fonts_links.rstrip()
        + "\n"
        + FONTS_NOSCRIPT
        + imgs
        + css_loader_block(core, pages)
        + "</head>"
    )
    text = text[: m.start()] + new_block + text[m.end() :]
    path.write_text(text, encoding="utf-8")
    return "fixed"


def verify(path: Path) -> None:
    t = path.read_text(encoding="utf-8")
    head = t[: t.find("</head>") + 7]
    boots = len(re.findall(r"var left=\d+", head))
    core = len(re.findall(r"styles\.min\.css", head))
    pages = len(re.findall(r"styles-pages\.min\.css", head))
    # Unclosed noscript? count open vs close in head
    opens = len(re.findall(r"<noscript>", head, re.I))
    closes = len(re.findall(r"</noscript>", head, re.I))
    print(
        f"{path.relative_to(ROOT)}: boots={boots} core={core} pages={pages} "
        f"noscript {opens}/{closes} crit_height_auto={'height:auto' in head and '.hero{' in head}"
    )


def main() -> None:
    counts: dict[str, int] = {}
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        if path.name.startswith("preview"):
            continue
        status = fix_file(path)
        counts[status] = counts.get(status, 0) + 1
        if status.startswith("fixed") or status == "no-tail":
            print(status, path.relative_to(ROOT))
    print("summary", counts)
    for rel in ("index.html", "kontakt.html", "hu/index.html", "preisliste.html"):
        verify(ROOT / rel)


if __name__ == "__main__":
    main()
