# -*- coding: utf-8 -*-
"""Turn footer brand mark into a home-top link (like navbar logo)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# <p class="footer__logo"><img ... /></p>  ->  <a href="..." class="footer__logo js-home-top"><img ... /></a>
FOOTER_LOGO_RE = re.compile(
    r'<p class="footer__logo">(\s*<img\s+[^>]*?Fati_logo\.svg[^>]*?>\s*)</p>',
    re.I,
)


def main() -> None:
    n = 0
    for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
        if path.name.startswith("preview"):
            continue
        text = path.read_text(encoding="utf-8")
        if "footer__logo" not in text or 'http-equiv="refresh"' in text[:1200]:
            continue
        href = "index.html"
        # already an anchor?
        if re.search(r'<a[^>]*class="footer__logo', text):
            # ensure js-home-top
            new = re.sub(
                r'(<a href="(?:\.\./)?index\.html" class="footer__logo)(")',
                r'\1 js-home-top\2',
                text,
                count=1,
            )
            new = re.sub(
                r'(<a href="(?:\.\./)?index\.html" class="footer__logo)(?! js-home-top)',
                r'\1 js-home-top',
                new,
                count=1,
            )
            if new != text:
                path.write_text(new, encoding="utf-8")
                n += 1
                print("patched a", path.relative_to(ROOT))
            continue

        def repl(m: re.Match[str]) -> str:
            return (
                f'<a href="{href}" class="footer__logo js-home-top">'
                f"{m.group(1)}"
                f"</a>"
            )

        new, count = FOOTER_LOGO_RE.subn(repl, text, count=1)
        if count:
            path.write_text(new, encoding="utf-8")
            n += 1
            print("ok", path.relative_to(ROOT))
        else:
            print("NO MATCH", path.relative_to(ROOT))
    print("total", n)


if __name__ == "__main__":
    main()
