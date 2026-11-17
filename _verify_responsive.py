# -*- coding: utf-8 -*-
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
bad = []
for path in list(ROOT.glob("*.html")) + list((ROOT / "hu").glob("*.html")):
    if path.name.startswith("preview"):
        continue
    t = path.read_text(encoding="utf-8")
    issues = []
    if "//>" in t:
        issues.append("double-slash")
    if re.search(r"/\s+srcset=", t):
        issues.append("slash-before-srcset")
    if path.name == "index.html" or path.parent.name == "hu" and path.name == "index.html":
        if "Hero_img-800.webp" not in t:
            issues.append("missing-hero-800")
        if "imagesrcset" not in t:
            issues.append("missing-imagesrcset")
    if issues:
        bad.append((str(path.relative_to(ROOT)), issues))
        print("BAD", path.relative_to(ROOT), issues)
    else:
        print("OK", path.relative_to(ROOT))

# sample sizes
for s in [
    "assets/imgs/Hero_img-800.webp",
    "assets/imgs/Hero_img.webp",
    "assets/imgs/page-gallery/pilla/szempilla-02-640.webp",
    "assets/imgs/page-gallery/pilla/szempilla-02.webp",
    "assets/imgs/page-gallery/pilla/szempilla-02.jpg",
]:
    p = ROOT / s
    print(f"{s}: {p.stat().st_size/1024:.1f}KB")
print("bad", len(bad))
