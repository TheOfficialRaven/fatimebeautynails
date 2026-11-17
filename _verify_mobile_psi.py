# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
IMGS = ROOT / "assets" / "imgs" / "Logo_Carousel"

for name in ("Alveola", "JB_lashes"):
    png = IMGS / f"{name}.png"
    webp = IMGS / f"{name}.webp"
    if not png.exists():
        continue
    im = Image.open(png).convert("RGBA")
    print(name, "png", im.size)
    w, h = im.size
    max_w = 440
    if w > max_w:
        nh = max(1, int(round(h * (max_w / w))))
        im = im.resize((max_w, nh), Image.Resampling.LANCZOS)
    im.save(webp, "WEBP", quality=72, method=6)
    print(name, "webp", round(webp.stat().st_size / 1024, 1), "KiB", im.size)

t = (ROOT / "index.html").read_text(encoding="utf-8")
a = t.find("/*critical*/")
b = t.find("</style>", a)
crit = t[a:b]
checks = {
    "crit mobile bg": "hero__image-bg img{left:0" in crit,
    "crit title white": "hero__title{color:#fff" in crit,
    "crit icon": "service-card__icon{width:3rem" in crit,
    "desktop bg full": 'srcset="assets/imgs/Hero_background_img.webp"' in t,
    "desktop hero full": 'srcset="assets/imgs/Hero_img.webp"' in t,
    "desktop rolam full": 'srcset="assets/imgs/Main_Rolam.webp"' in t,
    "no 1400 mobile 2x": "Hero_background_img-1400.webp 2x" not in t,
    "no 1200 mobile 2x": "Hero_img-1200.webp 2x" not in t,
    "preload mobile bg": "Hero_background_img-900.webp" in t and 'media="(max-width: 900px)"' in t,
    "bg fetchpriority": 'Hero_background_img.png" alt="" width="1200" height="800" loading="eager" decoding="async" fetchpriority="high"' in t,
    "gallery 400": "szempilla-02-400.webp 400w" in t,
    "gallery quote ok": 'szempilla-02.webp 1200w" sizes=' in t,
}
for k, v in checks.items():
    print(("OK" if v else "FAIL"), k)

min_css = (ROOT / "css" / "styles.min.css").read_text(encoding="utf-8")
print("min has hero img rule", ".hero__image-bg img{position:absolute" in min_css)
print("min has mobile overlay layout", "object-position:center center" in min_css and ".hero__media{grid-row:1" in min_css)
