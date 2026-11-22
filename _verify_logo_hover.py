# -*- coding: utf-8 -*-
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def minify_css(src: str) -> str:
    out = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    out = re.sub(r"\s+", " ", out)
    out = re.sub(r"\s*([{}:;,>])\s*", r"\1", out)
    return out.replace(";}", "}").strip()


(ROOT / "css" / "styles.min.css").write_text(
    minify_css((ROOT / "css" / "styles.css").read_text(encoding="utf-8")),
    encoding="utf-8",
)

for rel in ("index.html", "hu/index.html", "kontakt.html", "hu/kapcsolat.html"):
    t = (ROOT / rel).read_text(encoding="utf-8")
    ok = 'class="footer__logo js-home-top"' in t
    print(rel, "OK" if ok else "FAIL")

m = (ROOT / "css" / "styles.min.css").read_text(encoding="utf-8")
print("partners hover", "partners__item:hover .partners__logo" in m)
print("logo hover", ".logo:hover img" in m)
print("footer logo hover", ".footer__logo:hover img" in m)
