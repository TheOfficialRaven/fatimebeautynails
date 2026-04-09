#!/usr/bin/env python3
"""Pass 5: gallery alts (kép→Bild), HU HTML comments, stray strings. Root *.html only."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = [
    (
        '<p class="subpage-kicker">Schöne, gepflegte Füsse</p>\n          <h2 id="gallery-heading" class="section-title page-gallery-section__title">Sieh dir meine Referenzen an</h2>\n          <p class="section-subtitle page-gallery-section__intro">\n            Gepflegter Auftritt – echte Resultate in Bildern.\n          </p>\n        </header>\n        <!-- Galéria: képek az assets/imgs/page-gallery/lifting/',
        '<p class="subpage-kicker">Wimpern-Lifting &amp; Brauen</p>\n          <h2 id="gallery-heading" class="section-title page-gallery-section__title">Sieh dir meine Referenzen an</h2>\n          <p class="section-subtitle page-gallery-section__intro">\n            Gepflegter Auftritt – echte Resultate in Bildern.\n          </p>\n        </header>\n        <!-- Galerie: Bilder in assets/imgs/page-gallery/lifting/',
    ),
    (
        '<h2 id="gallery-heading" class="section-title page-gallery-section__title">Intenzív tekintet, természetes hatás</h2>',
        '<h2 id="gallery-heading" class="section-title page-gallery-section__title">Intensiver Blick, natürlicher Look</h2>',
    ),
    (
        'alt="Gästin bei der Gesichtsbehandlung — hero kép"',
        'alt="Gästin bei der Gesichtsbehandlung — Hero-Bild"',
    ),
    (
        '<span class="faq-item__question">Gibt es eine Garantie? (1&nbsp;hét)</span>',
        '<span class="faq-item__question">Gibt es eine Garantie? (1&nbsp;Woche)</span>',
    ),
    (
        "<!-- Placeholder képek a főoldalról / közös assetek; kattintásra ugyanaz a lightbox mint a referenciáknál. -->",
        "<!-- Platzhalterbilder von der Startseite / gemeinsame Assets; Klick öffnet dieselbe Lightbox wie bei den Referenzen. -->",
    ),
    (
        "<!-- Galéria: képek az ",
        "<!-- Galerie: Bilder in ",
    ),
    (
        " mappában (01.png–12.png). Csak erre az aloldalra cseréld őket. -->",
        " (01.png–12.png). Nur für diese Unterseite austauschen. -->",
    ),
]


def main():
    alt_re = re.compile(r'alt="([^"]+), (\d+)\. kép"')

    for path in sorted(ROOT.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        orig = text
        text = alt_re.sub(r'alt="\1, Bild \2"', text)
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print("updated", path.name)


if __name__ == "__main__":
    main()
