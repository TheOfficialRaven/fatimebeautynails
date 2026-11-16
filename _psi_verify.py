# -*- coding: utf-8 -*-
from pathlib import Path

root = Path(__file__).resolve().parent
bad = []
for p in list(root.glob("*.html")) + list((root / "hu").glob("*.html")):
    t = p.read_text(encoding="utf-8")
    if "bootstrap@" in t:
        bad.append((p.name, "bootstrap"))
    if "Hero_img.png" in t or "Hero_background_img.png" in t:
        bad.append((p.name, "hero png"))
    if 'href="css/styles.css"' in t or 'href="../css/styles.css"' in t:
        bad.append((p.name, "unmin css"))
print("bad", bad or "none")
print("hero webp KB", (root / "assets/imgs/Hero_img.webp").stat().st_size // 1024)
print("hero bg webp KB", (root / "assets/imgs/Hero_background_img.webp").stat().st_size // 1024)
print("styles.min has gold", "#8a7644" in (root / "css/styles.min.css").read_text(encoding="utf-8"))
print("index defer", "main.min.js\" defer" in (root / "index.html").read_text(encoding="utf-8"))
