# -*- coding: utf-8 -*-
"""Inject SEO head tags. Run from repo root: python _seo_apply.py"""
from __future__ import annotations

import re
from pathlib import Path

# Cseréld le az éles domainre, amikor él: pl. https://www.fatimebeautynails.ch
BASE = "https://fatimebeautynails.netlify.app"

# path (relative to repo), lang, title, description, og_image (site-relative), pair_de, pair_hu
PAGES = [
    # DE
    {
        "path": "index.html",
        "lang": "de",
        "title": "Fatime Beauty Nails | Kosmetik, Nails & Beauty in Arbon / Frasnacht (TG)",
        "description": "Beauty-Salon in Frasnacht bei Arbon (Thurgau): Maniküre, Pediküre, Kosmetik, Wimpern, Brauen und Piercing. Termine in der Region Arbon, Romanshorn und Umgebung.",
        "og_image": "/assets/imgs/Hero_img.png",
        "de": "/index.html",
        "hu": "/hu/index.html",
        "canonical": "/index.html",
        "home": True,
    },
    {
        "path": "kosmetische-behandlungen.html",
        "lang": "de",
        "title": "Kosmetische Behandlungen in Arbon / Frasnacht | Fatime Beauty Nails",
        "description": "Professionelle Gesichtsbehandlungen und Kosmetik in Frasnacht bei Arbon (TG). Individuelle Pflege mit Premium-Wirkstoffen – für die Region Arbon und Umgebung.",
        "og_image": "/assets/imgs/Hero_background_img.png",
        "de": "/kosmetische-behandlungen.html",
        "hu": "/hu/kozmetikai-kezelesek.html",
        "canonical": "/kosmetische-behandlungen.html",
    },
    {
        "path": "manikuere-modellage.html",
        "lang": "de",
        "title": "Maniküre & Modellage in Arbon / Frasnacht | Fatime Beauty Nails",
        "description": "Maniküre und Nagelmodellage in Frasnacht bei Arbon (Thurgau). Langanhaltende, präzise Nägel – Beauty-Salon in der Region Arbon.",
        "og_image": "/assets/imgs/Hero_background_img.png",
        "de": "/manikuere-modellage.html",
        "hu": "/hu/manikur-mukorom.html",
        "canonical": "/manikuere-modellage.html",
    },
    {
        "path": "callux-pedikuere.html",
        "lang": "de",
        "title": "Callux Pediküre in Arbon / Frasnacht | Fatime Beauty Nails",
        "description": "Sanfte Callux-Pediküre in Frasnacht bei Arbon (TG). Weiche, gepflegte Füsse ohne aggressive Chemie – Salon in der Region Arbon.",
        "og_image": "/assets/imgs/Hero_background_img.png",
        "de": "/callux-pedikuere.html",
        "hu": "/hu/callux-pedikur.html",
        "canonical": "/callux-pedikuere.html",
    },
    {
        "path": "wimpernlifting-brauen-laminierung.html",
        "lang": "de",
        "title": "Wimpern & Brauen in Arbon / Frasnacht | Fatime Beauty Nails",
        "description": "Wimpernlifting, Wimpernverlängerung und Brauenlaminierung in Frasnacht bei Arbon (Thurgau). Natürlicher Look – Beauty in der Region Arbon.",
        "og_image": "/assets/imgs/Hero_background_img.png",
        "de": "/wimpernlifting-brauen-laminierung.html",
        "hu": "/hu/szempilla-szemoldok-lifting.html",
        "canonical": "/wimpernlifting-brauen-laminierung.html",
    },
    {
        "path": "piercing.html",
        "lang": "de",
        "title": "Piercing in Arbon / Frasnacht | Fatime Beauty Nails",
        "description": "Steriles Ohr- und Nasenpiercing mit Premium-Schmuck in Frasnacht bei Arbon (TG). Schnell, hygienisch – Salon in der Region Arbon.",
        "og_image": "/assets/imgs/Hero_background_img.png",
        "de": "/piercing.html",
        "hu": "/hu/piercing.html",
        "canonical": "/piercing.html",
    },
    {
        "path": "preisliste.html",
        "lang": "de",
        "title": "Preisliste | Fatime Beauty Nails Arbon / Frasnacht (TG)",
        "description": "Aktuelle Preise für Kosmetik, Maniküre, Pediküre, Wimpern, Brauen und Piercing bei Fatime Beauty Nails in Frasnacht bei Arbon.",
        "og_image": "/assets/imgs/Hero_background_img.png",
        "de": "/preisliste.html",
        "hu": "/hu/arlista.html",
        "canonical": "/preisliste.html",
    },
    {
        "path": "kontakt.html",
        "lang": "de",
        "title": "Kontakt & Termin | Fatime Beauty Nails Arbon / Frasnacht",
        "description": "Kontakt und Terminvereinbarung bei Fatime Beauty Nails in Frasnacht bei Arbon (Thurgau). Schreib uns – wir melden uns schnell.",
        "og_image": "/assets/imgs/Kapcsolat_main.jpg",
        "de": "/kontakt.html",
        "hu": "/hu/kapcsolat.html",
        "canonical": "/kontakt.html",
    },
    {
        "path": "ueber-mich.html",
        "lang": "de",
        "title": "Über mich | Fatime Beauty Nails Arbon / Frasnacht (TG)",
        "description": "Fatime Gör-Nagy – Beauty-Expertin in Frasnacht bei Arbon. Persönliche Behandlungen mit über 7 Jahren Erfahrung in der Region Thurgau.",
        "og_image": "/assets/imgs/Rolam_main.jpg",
        "de": "/ueber-mich.html",
        "hu": "/hu/rolam.html",
        "canonical": "/ueber-mich.html",
    },
    {
        "path": "hausordnung.html",
        "lang": "de",
        "title": "Hausordnung | Fatime Beauty Nails Arbon / Frasnacht",
        "description": "Hausordnung von Fatime Beauty Nails in Frasnacht bei Arbon – damit Behandlungen ruhig und reibungslos ablaufen.",
        "og_image": "/assets/imgs/Hero_background_img.png",
        "de": "/hausordnung.html",
        "hu": "/hu/hazirend.html",
        "canonical": "/hausordnung.html",
    },
    {
        "path": "datenschutzerklaerung.html",
        "lang": "de",
        "title": "Datenschutzerklärung | Fatime Beauty Nails",
        "description": "Datenschutzerklärung von Fatime Beauty Nails in Frasnacht bei Arbon – Informationen zum Schutz personenbezogener Daten.",
        "og_image": "/assets/imgs/Hero_background_img.png",
        "de": "/datenschutzerklaerung.html",
        "hu": "/hu/adatkezelesi-tajekoztato.html",
        "canonical": "/datenschutzerklaerung.html",
    },
    # HU
    {
        "path": "hu/index.html",
        "lang": "hu",
        "title": "Fatime Beauty Nails | Kozmetika, köröm & beauty Arbon / Frasnacht (TG)",
        "description": "Szépségszalon Frasnachtban, Arbon mellett (Thurgau): manikűr, pedikűr, kozmetika, szempilla, szemöldök és piercing. Időpont a régióban – Arbon, Romanshorn és környéke.",
        "og_image": "/assets/imgs/Hero_img.png",
        "de": "/index.html",
        "hu": "/hu/index.html",
        "canonical": "/hu/index.html",
        "home": True,
    },
    {
        "path": "hu/kozmetikai-kezelesek.html",
        "lang": "hu",
        "title": "Kozmetikai kezelések Arbon / Frasnacht | Fatime Beauty Nails",
        "description": "Professzionális arckezelések és kozmetika Frasnachtban, Arbon mellett (TG). Személyre szabott ápolás prémium hatóanyagokkal a régióban.",
        "og_image": "/assets/imgs/Hero_background_img.png",
        "de": "/kosmetische-behandlungen.html",
        "hu": "/hu/kozmetikai-kezelesek.html",
        "canonical": "/hu/kozmetikai-kezelesek.html",
    },
    {
        "path": "hu/manikur-mukorom.html",
        "lang": "hu",
        "title": "Manikűr és műköröm Arbon / Frasnacht | Fatime Beauty Nails",
        "description": "Manikűr és műköröm Frasnachtban, Arbon mellett (Thurgau). Tartós, precíz körmök – szépségszalon az Arboni régióban.",
        "og_image": "/assets/imgs/Hero_background_img.png",
        "de": "/manikuere-modellage.html",
        "hu": "/hu/manikur-mukorom.html",
        "canonical": "/hu/manikur-mukorom.html",
    },
    {
        "path": "hu/callux-pedikur.html",
        "lang": "hu",
        "title": "Callux pedikűr Arbon / Frasnacht | Fatime Beauty Nails",
        "description": "Gyengéd Callux pedikűr Frasnachtban, Arbon mellett (TG). Selymes, ápolt lábak – szalon az Arboni régióban.",
        "og_image": "/assets/imgs/Hero_background_img.png",
        "de": "/callux-pedikuere.html",
        "hu": "/hu/callux-pedikur.html",
        "canonical": "/hu/callux-pedikur.html",
    },
    {
        "path": "hu/szempilla-szemoldok-lifting.html",
        "lang": "hu",
        "title": "Szempilla és szemöldök Arbon / Frasnacht | Fatime Beauty Nails",
        "description": "Szempilla lifting, műszempilla és szemöldök laminálás Frasnachtban, Arbon mellett (Thurgau). Természetes hatás az Arboni régióban.",
        "og_image": "/assets/imgs/Hero_background_img.png",
        "de": "/wimpernlifting-brauen-laminierung.html",
        "hu": "/hu/szempilla-szemoldok-lifting.html",
        "canonical": "/hu/szempilla-szemoldok-lifting.html",
    },
    {
        "path": "hu/piercing.html",
        "lang": "hu",
        "title": "Piercing Arbon / Frasnacht | Fatime Beauty Nails",
        "description": "Steril fül- és orrpiercing prémium ékszerrel Frasnachtban, Arbon mellett (TG). Gyors, higiénikus – szalon az Arboni régióban.",
        "og_image": "/assets/imgs/Hero_background_img.png",
        "de": "/piercing.html",
        "hu": "/hu/piercing.html",
        "canonical": "/hu/piercing.html",
    },
    {
        "path": "hu/arlista.html",
        "lang": "hu",
        "title": "Árlista | Fatime Beauty Nails Arbon / Frasnacht (TG)",
        "description": "Aktuális árak: kozmetika, manikűr, pedikűr, szempilla, szemöldök és piercing – Fatime Beauty Nails Frasnachtban, Arbon mellett.",
        "og_image": "/assets/imgs/Hero_background_img.png",
        "de": "/preisliste.html",
        "hu": "/hu/arlista.html",
        "canonical": "/hu/arlista.html",
    },
    {
        "path": "hu/kapcsolat.html",
        "lang": "hu",
        "title": "Kapcsolat és időpont | Fatime Beauty Nails Arbon / Frasnacht",
        "description": "Kapcsolat és időpontfoglalás a Fatime Beauty Nails-nál Frasnachtban, Arbon mellett (Thurgau). Írj – hamarosan jelentkezünk.",
        "og_image": "/assets/imgs/Kapcsolat_main.jpg",
        "de": "/kontakt.html",
        "hu": "/hu/kapcsolat.html",
        "canonical": "/hu/kapcsolat.html",
    },
    {
        "path": "hu/rolam.html",
        "lang": "hu",
        "title": "Rólam | Fatime Beauty Nails Arbon / Frasnacht (TG)",
        "description": "Fatime Gör-Nagy – szépségápolási szakember Frasnachtban, Arbon mellett. Személyre szabott kezelések 7+ év tapasztalattal Thurgauban.",
        "og_image": "/assets/imgs/Rolam_main.jpg",
        "de": "/ueber-mich.html",
        "hu": "/hu/rolam.html",
        "canonical": "/hu/rolam.html",
    },
    {
        "path": "hu/hazirend.html",
        "lang": "hu",
        "title": "Házirend | Fatime Beauty Nails Arbon / Frasnacht",
        "description": "A Fatime Beauty Nails házirendje Frasnachtban, Arbon mellett – a nyugodt, zökkenőmentes kezelésekért.",
        "og_image": "/assets/imgs/Hero_background_img.png",
        "de": "/hausordnung.html",
        "hu": "/hu/hazirend.html",
        "canonical": "/hu/hazirend.html",
    },
    {
        "path": "hu/adatkezelesi-tajekoztato.html",
        "lang": "hu",
        "title": "Adatkezelési tájékoztató | Fatime Beauty Nails",
        "description": "Adatkezelési tájékoztató – Fatime Beauty Nails Frasnacht / Arbon. Személyes adatok védelme a weboldalon és kapcsolatfelvétel során.",
        "og_image": "/assets/imgs/Hero_background_img.png",
        "de": "/datenschutzerklaerung.html",
        "hu": "/hu/adatkezelesi-tajekoztato.html",
        "canonical": "/hu/adatkezelesi-tajekoztato.html",
    },
]


def local_business_jsonld() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "BeautySalon",
        "name": "Fatime Beauty Nails",
        "image": f"{BASE}/assets/imgs/Hero_img.png",
        "url": f"{BASE}/",
        "telephone": "+41762183856",
        "email": "fatimegor8@gmail.com",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Frasnacht",
            "addressLocality": "Arbon",
            "postalCode": "9320",
            "addressRegion": "TG",
            "addressCountry": "CH",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 47.5167,
            "longitude": 9.4333,
        },
        "areaServed": [
            {"@type": "City", "name": "Arbon"},
            {"@type": "City", "name": "Frasnacht"},
            {"@type": "City", "name": "Romanshorn"},
            {"@type": "AdministrativeArea", "name": "Thurgau"},
        ],
        "sameAs": [
            "https://www.facebook.com/profile.php?id=61574023973561",
            "https://www.instagram.com/fatimegor/",
        ],
        "priceRange": "$$",
        "inLanguage": ["de", "hu"],
    }
    import json

    return (
        '<script type="application/ld+json">\n'
        + json.dumps(data, ensure_ascii=False, indent=2)
        + "\n</script>"
    )


def build_head_block(page: dict) -> str:
    canon = BASE + page["canonical"]
    de = BASE + page["de"]
    hu = BASE + page["hu"]
    og_img = BASE + page["og_image"]
    og_locale = "de_CH" if page["lang"] == "de" else "hu_HU"
    og_alt = "hu_HU" if page["lang"] == "de" else "de_CH"
    title = page["title"]
    desc = page["description"]

    lines = [
        f"<title>{title}</title>",
        f'<meta name="description" content="{desc}" />',
        '<meta name="robots" content="index, follow, max-image-preview:large" />',
        '<meta name="geo.region" content="CH-TG" />',
        '<meta name="geo.placename" content="Arbon, Frasnacht" />',
        '<meta name="geo.position" content="47.5167;9.4333" />',
        '<meta name="ICBM" content="47.5167, 9.4333" />',
        f'<link rel="canonical" href="{canon}" />',
        f'<link rel="alternate" hreflang="de" href="{de}" />',
        f'<link rel="alternate" hreflang="hu" href="{hu}" />',
        f'<link rel="alternate" hreflang="x-default" href="{de}" />',
        f'<meta property="og:type" content="website" />',
        f'<meta property="og:locale" content="{og_locale}" />',
        f'<meta property="og:locale:alternate" content="{og_alt}" />',
        f'<meta property="og:site_name" content="Fatime Beauty Nails" />',
        f'<meta property="og:title" content="{title}" />',
        f'<meta property="og:description" content="{desc}" />',
        f'<meta property="og:url" content="{canon}" />',
        f'<meta property="og:image" content="{og_img}" />',
        f'<meta name="twitter:card" content="summary_large_image" />',
        f'<meta name="twitter:title" content="{title}" />',
        f'<meta name="twitter:description" content="{desc}" />',
        f'<meta name="twitter:image" content="{og_img}" />',
    ]
    if page.get("home"):
        lines.append(local_business_jsonld())
    return "\n  ".join(lines)


SEO_START = "<!-- SEO:start -->"
SEO_END = "<!-- SEO:end -->"


def strip_old_seo(html: str) -> str:
    # Remove previous injected block
    html = re.sub(
        r"\s*" + re.escape(SEO_START) + r".*?" + re.escape(SEO_END) + r"\s*",
        "\n",
        html,
        flags=re.S,
    )
    # Remove existing title / description / canonical / hreflang / og / twitter / geo / ld+json BeautySalon
    patterns = [
        r"<title>.*?</title>\s*",
        r'<meta\s+name="description"[^>]*>\s*',
        r'<meta\s+name="robots"[^>]*>\s*',
        r'<meta\s+name="geo\.[^"]*"[^>]*>\s*',
        r'<meta\s+name="ICBM"[^>]*>\s*',
        r'<link\s+rel="canonical"[^>]*>\s*',
        r'<link\s+rel="alternate"[^>]*hreflang="[^"]*"[^>]*>\s*',
        r'<meta\s+property="og:[^"]*"[^>]*>\s*',
        r'<meta\s+name="twitter:[^"]*"[^>]*>\s*',
        r'<script\s+type="application/ld\+json">.*?</script>\s*',
    ]
    for pat in patterns:
        html = re.sub(pat, "", html, flags=re.I | re.S)
    return html


def apply_page(page: dict) -> None:
    path = Path(page["path"])
    html = path.read_text(encoding="utf-8")
    html = strip_old_seo(html)
    block = f"  {SEO_START}\n  {build_head_block(page)}\n  {SEO_END}\n"

    # Insert after favicon / shortcut icon block, or after viewport
    m = re.search(
        r'(<link\s+rel="shortcut icon"[^>]*>\s*)',
        html,
        flags=re.I,
    )
    if m:
        html = html[: m.end()] + block + html[m.end() :]
    else:
        m = re.search(r'(<meta\s+name="viewport"[^>]*>\s*)', html, flags=re.I)
        if not m:
            raise RuntimeError(f"No insert point in {path}")
        html = html[: m.end()] + block + html[m.end() :]

    path.write_text(html, encoding="utf-8")
    print("OK", path)


def write_robots_and_sitemap() -> None:
    Path("robots.txt").write_text(
        f"""User-agent: *
Allow: /

Sitemap: {BASE}/sitemap.xml
""",
        encoding="utf-8",
    )

    urls = []
    for p in PAGES:
        # Skip pure legal pages from high priority but include them
        priority = "1.0" if p.get("home") else ("0.9" if "kontakt" in p["path"] or "kapcsolat" in p["path"] or "preisliste" in p["path"] or "arlista" in p["path"] else "0.8")
        if "datenschutz" in p["path"] or "adatkezelesi" in p["path"] or "hausordnung" in p["path"] or "hazirend" in p["path"]:
            priority = "0.3"
        urls.append(
            f"""  <url>
    <loc>{BASE}{p['canonical']}</loc>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
  </url>"""
        )

    Path("sitemap.xml").write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""
        + "\n".join(urls)
        + "\n</urlset>\n",
        encoding="utf-8",
    )
    print("OK robots.txt, sitemap.xml")


def main() -> None:
    for page in PAGES:
        apply_page(page)
    write_robots_and_sitemap()
    print("Done. BASE =", BASE)
    print("Éles domainnél cseréld a BASE-t ebben a fájlban, majd futtasd újra.")


if __name__ == "__main__":
    main()
