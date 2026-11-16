# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image

IMGS = Path(r"e:\HTML\fatimebeautynails új design\assets\imgs")
samples = [
    "page-gallery/manikur/manikur-21.jpg",
    "page-gallery/kozmetikai/kozmetikai-06.jpg",
    "page-gallery/pilla/szempilla-02.jpg",
    "Main_Rolam.jpg",
    "Main_kapcsolat.jpg",
    "Main_kapcsolat.webp",
]
for rel in samples:
    src = IMGS / rel
    if not src.exists():
        print("missing", rel)
        continue
    im = Image.open(src)
    print(rel, im.size, round(src.stat().st_size / 1024), "KB", im.mode)
