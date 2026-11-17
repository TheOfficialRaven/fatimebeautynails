# -*- coding: utf-8 -*-
from pathlib import Path
import re

t = Path("index.html").read_text(encoding="utf-8")
a = t.find("/*critical*/")
b = t.find("</style>", a)
c = t[a:b]
print("cqw margin", "100cqw" in c)
print("mid desktop", "min-width:901px" in c)
print("page-hero 175%", "height:175%" in c)
print("100cqw count", c.count("100cqw"))
m = re.search(r"Hero_background_img\.png[^>]+>", t)
print("bg:", m.group(0) if m else "no")
m2 = re.search(r'class="hero__image-figure"[\s\S]{0,120}?decoding="[^"]+"', t)
print("fig:", m2.group(0).replace("\n", " ") if m2 else "no")
