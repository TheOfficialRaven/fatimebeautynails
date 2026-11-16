# -*- coding: utf-8 -*-
import re
from pathlib import Path

IMGS = Path(r"e:\HTML\fatimebeautynails új design\assets\imgs")
root = Path(r"e:\HTML\fatimebeautynails új design")

for c in IMGS.glob("[Mm]anikur_3.*"):
    print("manikur3", c.name, round(c.stat().st_size / 1024))

left = set()
missing = []
for p in list(root.glob("*.html")) + list((root / "hu").glob("*.html")):
    text = p.read_text(encoding="utf-8")
    for m in re.findall(r'(?:\.\./)?assets/imgs/([^\"\']+\.(?:webp|jpg|jpeg|png|JPG|PNG))', text):
        if m.endswith(".webp"):
            left.add(m)
        path = IMGS / m.replace("/", "\\") if "\\" in m else IMGS / m
        # normalize
        path = IMGS.joinpath(*m.split("/"))
        if not path.exists():
            missing.append((p.name, m))

print("remaining webp refs:", sorted(left))
print("missing files:", missing[:20], "count", len(missing))
