# -*- coding: utf-8 -*-
"""Add Sogra Webstudio credit line to all footers."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CREDIT_DE = (
    '        <p class="footer__credit">'
    "Webseite erstellt von: "
    '<a href="https://sograwebstudio.com" class="footer__credit-link" '
    'target="_blank" rel="noopener noreferrer">Sogra Webstudio</a>'
    "</p>\n"
)

CREDIT_HU = (
    '        <p class="footer__credit">'
    "Weboldalt készítette: "
    '<a href="https://sograwebstudio.com" class="footer__credit-link" '
    'target="_blank" rel="noopener noreferrer">Sogra Webstudio</a>'
    "</p>\n"
)

# Insert before closing of footer__bar-inner, after footer__legal </p>
LEGAL_BLOCK_RE = re.compile(
    r'(<p class="footer__legal">[\s\S]*?</p>\s*)(</div>\s*</div>\s*</footer>)',
    re.I,
)


def main() -> None:
    n = 0
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        if path.name.startswith("preview"):
            continue
        text = path.read_text(encoding="utf-8")
        if "footer__credit" in text or "footer__legal" not in text:
            continue
        if 'http-equiv="refresh"' in text[:1200]:
            continue
        credit = CREDIT_HU if path.parent.name == "hu" else CREDIT_DE
        new, count = LEGAL_BLOCK_RE.subn(rf"\1{credit}      \2", text, count=1)
        if count:
            path.write_text(new, encoding="utf-8")
            n += 1
            print("ok", path.relative_to(ROOT))
        else:
            print("NO MATCH", path.relative_to(ROOT))
    print("total", n)


if __name__ == "__main__":
    main()
