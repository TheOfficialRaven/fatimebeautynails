# -*- coding: utf-8 -*-
"""Split page-only CSS out of styles.css into styles-pages.css."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "css" / "styles.css"
PAGES = ROOT / "css" / "styles-pages.css"

# Markers (inclusive start comment → exclusive end comment / EOF)
BLOCKS = [
    (
        "/* ——— Rólam: drótváz szerinti „masonry” (2×3 rács, szimmetrikus fordított T-rövid / rövid-T) ——— */",
        "/* ——— Referenciák / galéria lightbox (site modal overlay + lapozó) ——— */",
    ),
    (
        "/* ——— Aloldal: Kozmetikai kezelések ——— */",
        "/* ——— Welcome coupon popup ——— */",
    ),
]


def extract_blocks(text: str) -> tuple[str, str]:
    pages_chunks: list[str] = []
    remaining = text
    # Process from end so earlier indices stay valid... actually use iterative find on remaining
    for start_marker, end_marker in BLOCKS:
        start = remaining.find(start_marker)
        if start < 0:
            raise SystemExit(f"Missing start marker: {start_marker[:40]}")
        end = remaining.find(end_marker, start)
        if end < 0:
            raise SystemExit(f"Missing end marker: {end_marker[:40]}")
        chunk = remaining[start:end].rstrip() + "\n\n"
        pages_chunks.append(chunk)
        remaining = remaining[:start] + remaining[end:]

    # Also move early page-hero image-bg block (between home hero comments)
    early_start = "/* Aloldal: jobb oldalról a szöveg alá tolódik szűküléskor (mint a főoldal hero) */"
    early_end = "/* Előtér: transzparens PNG, ahol üres, átlátszik a háttér */"
    s = remaining.find(early_start)
    e = remaining.find(early_end)
    if s >= 0 and e > s:
        pages_chunks.insert(0, remaining[s:e].rstrip() + "\n\n")
        remaining = remaining[:s] + remaining[e:]

    header = (
        "/* Page-specific styles — loaded only on subpages (not homepage). */\n"
        "/* Extracted from styles.css to reduce unused CSS on the home LCP path. */\n\n"
    )
    pages_css = header + "".join(pages_chunks)
    # tidy double blank lines
    remaining = re.sub(r"\n{3,}", "\n\n", remaining)
    pages_css = re.sub(r"\n{3,}", "\n\n", pages_css)
    return remaining, pages_css


def main() -> None:
    if PAGES.exists() and "Page-specific styles" in PAGES.read_text(encoding="utf-8")[:200]:
        # Idempotent: if already split, rebuild pages from markers only if still in styles.css
        text = SRC.read_text(encoding="utf-8")
        if "/* ——— Aloldal: Kozmetikai kezelések ——— */" not in text:
            print("already split; styles.css has no aloldal block")
            return

    text = SRC.read_text(encoding="utf-8")
    core, pages = extract_blocks(text)
    SRC.write_text(core, encoding="utf-8")
    PAGES.write_text(pages, encoding="utf-8")
    print("styles.css KB", round(SRC.stat().st_size / 1024, 1))
    print("styles-pages.css KB", round(PAGES.stat().st_size / 1024, 1))


if __name__ == "__main__":
    main()
