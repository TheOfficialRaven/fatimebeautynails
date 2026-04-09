# -*- coding: utf-8 -*-
"""Apply German UI strings to root-level HTML (default language DE). Skips hu/."""
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Order: longer phrases first. Avoid substring traps (e.g. Ár inside Árak).
REPLACEMENTS = [
    ("<html lang=\"hu\">", "<html lang=\"de\">"),
    ('aria-label="Menü megnyitása"', 'aria-label="Menü öffnen"'),
    ('aria-label="Fő navigáció"', 'aria-label="Hauptnavigation"'),
    ('aria-label="Szolgáltatások almenü"', 'aria-label="Untermenü Leistungen"'),
    ('aria-label="Infó almenü"', 'aria-label="Untermenü Info"'),
    ("Szolgáltatások", "Leistungen"),
    ("Kozmetikai kezelések", "Kosmetische Behandlungen"),
    ("Manikűr és műköröm", "Maniküre &amp; Modellage"),
    ("Callux pedikűr", "Callux-Pediküre"),
    ("Szempilla lifting &amp; szemöldök laminálás", "Wimpernlifting &amp; Brauen-Lamination"),
    ("Pilla", "Wimpern"),
    ("Infó", "Info"),
    ("Árlista", "Preisliste"),
    ("Házirend", "Hausordnung"),
    ("Rólam", "Über mich"),
    ("Főoldal", "Startseite"),
    ("Kapcsolat", "Kontakt"),
    ("Minden jog fenntartva!", "Alle Rechte vorbehalten."),
    ("Adatkezelési tájékoztató", "Datenschutzerklärung"),
    ("Elérhetőség", "Kontakt"),
    ("Közösségi média", "Social Media"),
    ("Kövess minket", "Folge uns"),
    ("Facebook oldal megnyitása", "Facebook-Seite öffnen"),
    ("Instagram profil megnyitása", "Instagram-Profil öffnen"),
    ("Teljes név", "Vollständiger Name"),
    ('placeholder="Teljes név"', 'placeholder="Vollständiger Name"'),
    ('placeholder="E-mail cím"', 'placeholder="E-Mail-Adresse"'),
    ('placeholder="Üzenet"', 'placeholder="Nachricht"'),
    ("<span class=\"field__label\">Üzenet</span>", "<span class=\"field__label\">Nachricht</span>"),
    ("<span class=\"field__label\">Email</span>", "<span class=\"field__label\">E-Mail</span>"),
    ("KÜLDÉS", "SENDEN"),
    ("Elolvastam és elfogadom az", "Ich habe die"),
    ("adatkezelési tájékoztatót.", "Datenschutzerklärung gelesen und akzeptiere sie."),
    ("Gyakran Ismételt Kérdések", "Häufig gestellte Fragen"),
    ("Vendégparkoló", "Gastparkplatz"),
    ("IDŐPONTOT KÉREK", "TERMIN ANFRAGEN"),
    ("Időpontfoglalás", "Terminbuchung"),
    ("Tudj meg többet", "Mehr erfahren"),
    ("Referenciáink", "Referenzen"),
    ("Professzionális szépségápolási szolgáltatások személyre szabott megközelítéssel.", "Professionelle Beauty-Services mit persönlicher Beratung."),
    ("Kozmetika", "Kosmetik"),
    ("Manikűr &amp; műköröm", "Maniküre &amp; Modellage"),
    ("Szempilla építés", "Wimpernverlängerung"),
    ("Megnevezés", "Bezeichnung"),
    ('scope="col">Ár</th>', 'scope="col">Preis</th>'),
    ("Szolgáltatás", "Leistung"),
    ("Arc &amp; nyak", "Gesicht &amp; Hals"),
    ("+Dekolletés", "+Dekolleté"),
    ("Nyelvválasztó", "Sprachauswahl"),
    ("Árak", "Preise"),
]

# Second pass: strings that might conflict if done in wrong order — apply alone
EXTRA: list[tuple[str, str]] = [
    ('aria-roledescription="karousel"', 'aria-roledescription="Karussell"'),
    ('aria-label="Vendégvélemények"', 'aria-label="Kundenstimmen"'),
    ('aria-label="Válassz véleményt"', 'aria-label="Kundenstimme wählen"'),
    ('aria-label="Válassz oldalt (két vélemény)"', 'aria-label="Seite wählen (zwei Stimmen)"'),
    ("Előző vélemény", "Vorherige Kundenstimme"),
    ("Következő vélemény", "Nächste Kundenstimme"),
    ("Előző oldal", "Vorherige Seite"),
    ("Következő oldal", "Nächste Seite"),
    ("Referenciakép nagyítva", "Referenzbild vergrößert"),
    ("Bezárás", "Schließen"),
    ("Előző kép", "Vorheriges Bild"),
    ("Következő kép", "Nächstes Bild"),
    ("Partnerek", "Partner"),
]


def apply_to_file(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    orig = s
    for old, new in REPLACEMENTS:
        s = s.replace(old, new)
    for old, new in EXTRA:
        s = s.replace(old, new)
    if s != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
        return 1
    return 0


def main():
    n = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        if os.path.dirname(path) != ROOT:
            continue
        if apply_to_file(path):
            n += 1
            print("updated", os.path.basename(path))
    print("done, files changed:", n)


if __name__ == "__main__":
    main()
