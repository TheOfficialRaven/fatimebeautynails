#!/usr/bin/env python3
"""Fourth pass: remaining Hungarian snippets on root *.html only (never hu/)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS_RAW = [
    # —— Shared footer / about ——
    (
        "Fatime Beauty — professzionális szépségápolás, személyre szabott kezelésekkel és tiszteletteljes vendégközpontú hozzáállással.",
        "Fatime Beauty – professionelle Beauty-Pflege, massgeschneiderte Behandlungen und ein respektvoller, gästeorientierter Ansatz.",
    ),
    (
        "Személyre szabott kozmetikai kezelések bőrfiatalításra és problémás bőr kezelésére, modern technológiákkal és természetes hatóanyagokkal.",
        "Individuelle Kosmetik für Hautverjüngung und Problemhaut – mit modernen Methoden und natürlichen Wirkstoffen.",
    ),
    # —— Callux + Pilla quick fixes ——
    (
        "Callux-Pediküre és lábápolás — kíméletes technika, steril eszközök és személyre szabott tanácsadás az ápolt lábfejért.",
        "Callux-Pediküre und Fußpflege – schonende Technik, sterile Instrumente und persönliche Beratung für gepflegte Füsse.",
    ),
    ("?text=Pedikűr';", "?text=Pedikuere';"),
    ("Tartós, esztétikus és kényelmes viselet", "Haltbar, ästhetisch und angenehm zu tragen"),
    # —— Szempilla / Lifting ——
    (
        "Sieh dir unsere Preisliste für Lifting &amp; Pediküre an!",
        "Sieh dir unsere Preisliste für Wimpern- und Brauenlifting an!",
    ),
    ('alt="Szempilla lifting kezelés közben, részlet"', 'alt="Wimpernlifting während der Behandlung, Detail"'),
    ('alt="Brauen-Lamination kezelés közben, részlet"', 'alt="Brauen-Lamination während der Behandlung, Detail"'),
    ("?text=Laminálás';", "?text=Laminierung';"),
    # —— Piercing ——
    (
        "A hangsúlyos, mégis harmonikus tekintet a hétköznapokban is.",
        "Ausdrucksstarker, dennoch harmonischer Blick – auch im Alltag.",
    ),
    ("<p class=\"subpage-kicker\">Schöne, gepflegte Füsse</p>\n          <h2 id=\"gallery-heading\" class=\"section-title page-gallery-section__title\">Sieh dir meine Referenzen an</h2>\n          <p class=\"section-subtitle page-gallery-section__intro\">\n            Gepflegter Auftritt – echte Resultate in Bildern.\n          </p>\n        </header>\n        <!-- Galéria: képek az assets/imgs/page-gallery/piercing/",
        "<p class=\"subpage-kicker\">Piercing &amp; Schmuck</p>\n          <h2 id=\"gallery-heading\" class=\"section-title page-gallery-section__title\">Sieh dir meine Referenzen an</h2>\n          <p class=\"section-subtitle page-gallery-section__intro\">\n            Gepflegter Auftritt – echte Resultate in Bildern.\n          </p>\n        </header>\n        <!-- Galéria: képek az assets/imgs/page-gallery/piercing/",
    ),
    # —— Manikür (mixed HU/DE + sections) ——
    (
        "Tartós, rendezett és esztétikus megoldás a hétköznapokra is.",
        "Haltbare, ordentliche und ästhetische Lösungen – auch für den Alltag.",
    ),
    (
        "Ápolt kezek, magabiztos megjelenés",
        "Gepflegte Hände, selbstbewusster Auftritt",
    ),
    (
        "            Akril és gél technikával dolgozom, hogy a természetes köröm vagy épített köröm is tökéletes, tartós és esztétikus legyen. A kezelések\n            dabei achte ich auf jedes Detail – ob Alltag oder besonderer Anlass.\n",
        "            Mit Acryl- und Geltechnik arbeite ich daran, dass natürliche oder modellierte Nägel perfekt, haltbar und schön wirken. Dabei achte ich auf jedes Detail – ob Alltag oder besonderer Anlass.\n",
    ),
    ("Gél lakk: rugalmas, természetes hatású megjelenés", "Gel-Lack: flexibel, natürlich wirkend"),
    (
        "Mindennapi viseletre és alkalmakra egyaránt tökéletes",
        "Perfekt für Alltag und besondere Anlässe",
    ),
    ("Tekintsd meg kozmetikai árlistánkat!", "Sieh dir unsere Maniküre-Preisliste an!"),
    ("href=\"arlista.html#price-manikur\">ÁRLISTA &gt;", 'href="arlista.html#price-manikur">PREISE &gt;'),
    (
        "            Forma és hossz igény szerint, stabil alappal és szép ívekkel. Ideális, ha tartós, karakteres körmöt szeretnél — mindig a kezed\n            adottságaihoz és a mindennapi tevékenységeidhez igazítva.\n",
        "            Form und Länge nach Wunsch, mit stabiler Basis und schönen Schwüngen. Ideal, wenn du haltbare, charakterstarke Nägel möchtest – immer angepasst an deine Hände und deinen Alltag.\n",
    ),
    ('alt="Gél lakkozott körmök"', 'alt="Mit Gel-Lack lackierte Nägel"'),
    (
        "            Fényes, tartós szín hetekre — gyorsabb ütemben, mint a hagyományos lakkozás. Tökéletes választás, ha szereted a változatosságot, mégis\n            stabil, kifutásmentes eredményre vágysz.\n",
        "            Glänzende, haltbare Farbe für Wochen – schneller als klassisches Lackieren. Perfekt, wenn du Abwechslung magst und dennoch ein stabiles, auslauffreies Ergebnis willst.\n",
    ),
    ("<h2 id=\"svc-gel-title\" class=\"service-showcase__title section-title\">Gél lakk</h2>", '<h2 id="svc-gel-title" class="service-showcase__title section-title">Gel-Lack</h2>'),
    ("?text=Gél+lakk';", "?text=Gel+Lack';"),
    ("?text=Műköröm';", "?text=Modellage';"),
    ("?text=Japán+manikűr';", "?text=Japan+Manikuere';"),
    ("?text=Manikűr';", "?text=Manikuere';"),
    (
        '<h2 id="svc-manikur-title" class="service-showcase__title section-title">Manikűr</h2>',
        '<h2 id="svc-manikur-title" class="service-showcase__title section-title">Maniküre</h2>',
    ),
    ("<p class=\"subpage-kicker\">Szépség, ami csillog</p>", '<p class="subpage-kicker">Schönheit, die strahlt</p>'),
    (
        "            Ápolt, stílusos megjelenés - valódi eredmények képekben.\n",
        "            Gepflegter, stilvoller Look – echte Resultate in Bildern.\n",
    ),
    # —— Kozmetikai (large) ——
    (
        "            A kezelések során a bőr mélytisztítása, feszesítése és regenerálása történik, míg a professzionális termékek, manuális és gépi\n            technikák kombinációjával. Legkorszerűbb hatóanyagokkal dolgozom, hogy a bőröd hosszú távon is ápolt, kiegyensúlyozott és\n            ragyogó maradjon.\n",
        "            Dabei wird die Haut tief gereinigt, gestrafft und regeneriert – mit Profi-Produkten sowie manuellen und Gerätetechniken. Ich arbeite mit modernsten Wirkstoffen, damit deine Haut langfristig gepflegt, ausgeglichen und strahlend bleibt.\n",
    ),
    ('alt="Konzultáció a szalonban"', 'alt="Beratung im Salon"'),
    ("?text=Konzultáció';", "?text=Beratung';"),
    (
        "Professzionális szakértelem, fényesebb önbizalom",
        "Professionelle Expertise, strahlendes Selbstvertrauen",
    ),
    ("<span>Személyre szabott kezelés</span>", "<span>Individuelle Behandlung</span>"),
    ("<span>Hegkezelés</span>", "<span>Narbenpflege</span>"),
    ("<span>Hosszantartó eredmények</span>", "<span>Langanhaltende Ergebnisse</span>"),
    ("<span>Professzionális termékek</span>", "<span>Profi-Produkte</span>"),
    (
        "<h2 id=\"process-title\" class=\"section-title section-title--on-dark process-section__title\">Hogyan zajlik egy kezelés?</h2>",
        '<h2 id="process-title" class="section-title section-title--on-dark process-section__title">Wie läuft eine Behandlung ab?</h2>',
    ),
    (
        "            Professzionális szépségápolási szolgáltatások személyre szabott megközelítéssel\n",
        "            Professionelle Beauty-Services mit persönlichem Ansatz\n",
    ),
    (
        "<h3 class=\"process-card__title\">Kosmetiki kezelés</h3>",
        '<h3 class="process-card__title">Kosmetische Behandlung</h3>',
    ),
    (
        "<h3 class=\"process-card__title\">Tanácsok otthonra</h3>",
        '<h3 class="process-card__title">Tipps für zu Hause</h3>',
    ),
    ('alt="Manuális kozmetikai kezelés közben"', 'alt="Manuelle Kosmetikbehandlung"'),
    ("?text=Kezelés';", "?text=Behandlung';"),
    (
        "<h2 id=\"svc-a-title\" class=\"service-showcase__title section-title\">Manuális kozmetikai kezelések</h2>",
        '<h2 id="svc-a-title" class="service-showcase__title section-title">Manuelle Kosmetikbehandlungen</h2>',
    ),
    (
        "<span class=\"service-panel__title\">Eszter G-arckezelés | 1 óra</span>",
        '<span class="service-panel__title">Eszter G Gesichtsbehandlung | 1 Std.</span>',
    ),
    (
        "                          Személyre szabott arckezelés tisztítással, peelinggel és tápláló lépésekkel — a bőröd aktuális állapotához igazítva,\n                          prémium hatóanyagokkal.\n",
        "                          Individuelle Gesichtsbehandlung mit Reinigung, Peeling und nährenden Schritten – abgestimmt auf den aktuellen Zustand deiner Haut, mit Premium-Wirkstoffen.\n",
    ),
    (
        "<span class=\"service-panel__title\">Hagyományos arctisztítás | 1,5 óra</span>",
        '<span class="service-panel__title">Klassische Gesichtsreinigung | 1,5 Std.</span>',
    ),
    (
        "                          Alapos mitesszer- és komedókezelés, gyengéd hámlasztás és nyugtató pakolás — higiénikus, kíméletes technikával, hogy a bőr\n                          friss és tiszta maradjon.\n",
        "                          Gründliche Mitesser- und Komedonenbehandlung, sanftes Peeling und beruhigende Maske – hygienisch und schonend, damit die Haut frisch und rein bleibt.\n",
    ),
    (
        "<span class=\"service-panel__title\">Prémium hidratáló kezelés | 50 perc</span>",
        '<span class="service-panel__title">Premium-Feuchtigkeitsbehandlung | 50 Min.</span>',
    ),
    (
        "                          Intenzív hidratálás és feszesítő hatóanyagok egy ülésben — ideális fakó, vízhiányos bőrre, látványos puhaságért és ragyogásért.\n",
        "                          Intensive Feuchtigkeit und straffende Wirkstoffe in einer Sitzung – ideal für blasse, feuchtigkeitsarme Haut, für spürbar weiche Haut und mehr Glanz.\n",
    ),
    ('alt="Gépi kozmetikai kezelés"', 'alt="Gerätegestützte Kosmetikbehandlung"'),
    ("?text=Gépi';", "?text=Geraet';"),
    (
        "<h2 id=\"svc-b-title\" class=\"service-showcase__title section-title\">Gépi kozmetika</h2>",
        '<h2 id="svc-b-title" class="service-showcase__title section-title">Gerätekosmetik</h2>',
    ),
    (
        "<span class=\"service-panel__title\">Ultrahangos arckezelés | 45 perc</span>",
        '<span class="service-panel__title">Ultraschall-Gesichtsbehandlung | 45 Min.</span>',
    ),
    (
        "                          Mélyebb rétegekbe juttatott hatóanyag-koktél ultrahanggal — gyorsabb felszívódás, kíméletes kezelés, ragyogóbb bőrkép.\n",
        "                          Wirkstoff-Cocktail tiefer in die Haut mit Ultraschall – schnellere Aufnahme, schonende Behandlung, strahlendere Haut.\n",
    ),
    (
        "<span class=\"service-panel__title\">Mikrodermabrázió | 50 perc</span>",
        '<span class="service-panel__title">Mikrodermabrasion | 50 Min.</span>',
    ),
    (
        "                          Finom hámlasztás a simább bőrfelszínért és az egyenetlenségek csökkentéséért — előzetes egyeztetéssel, bőrtípusodnak megfelelő\n                          erősséggel.\n",
        "                          Sanftes Peeling für eine glattere Hautoberfläche und weniger Unregelmässigkeiten – nach Absprache, in der Stärke passend zu deinem Hauttyp.\n",
    ),
    (
        '<span class="service-panel__title">Vákuumos mélytisztítás | 45 perc</span>',
        '<span class="service-panel__title">Vakuum-Tiefenreinigung | 45 Min.</span>',
    ),
    (
        "                          Finom vákuumos technika a pórusok tisztítására és a bőr frissítésére — kiegészítő lépésekkel a nyugodt, kipihent érzésért.\n",
        "                          Sanfte Vakuumtechnik zur Porenreinigung und Erfrischung der Haut – mit ergänzenden Schritten für ein ruhiges, ausgeruhtes Gefühl.\n",
    ),
    ('alt="További kozmetikai kezelések"', 'alt="Weitere kosmetische Behandlungen"'),
    (
        "<h2 id=\"svc-c-title\" class=\"service-showcase__title section-title\">További kozmetikai kezelések</h2>",
        '<h2 id="svc-c-title" class="service-showcase__title section-title">Weitere kosmetische Behandlungen</h2>',
    ),
    (
        "<span class=\"service-panel__title\">Szempilla és szemöldök festés | 45 perc</span>",
        '<span class="service-panel__title">Wimpern- und Brauenfärbung | 45 Min.</span>',
    ),
    (
        "                          Természetes hatású vagy karakteresebb szín — a szemöldök formájához és a pilláidhoz igazítva, tartós, egyenletes eredménnyel.\n",
        "                          Natürlicher oder ausdrucksstärkerer Farbton – abgestimmt auf deine Brauenform und Wimpern, mit haltbarem, gleichmässigem Ergebnis.\n",
    ),
    (
        "<span class=\"service-panel__title\">Smink (alkalmi / nappali) | 1 óra</span>",
        '<span class="service-panel__title">Make-up (Anlass / Day) | 1 Std.</span>',
    ),
    (
        "                          Egyénre szabott smink bőrtípusodhoz és az alkalomhoz — tartós finish, természetes vagy hangsúlyos megjelenés, igény szerint.\n",
        "                          Individuelles Make-up passend zu Hauttyp und Anlass – haltbarer Finish, natürlich oder betont, nach Wunsch.\n",
    ),
    (
        "<span class=\"service-panel__title\">Gyanta | testrész szerint</span>",
        '<span class="service-panel__title">Waxing | je nach Körperzone</span>',
    ),
    (
        "<p>Gyors, higiénikus szőrtelenítés prémium gyantával — a kezelt területnek megfelelő technikával.</p>",
        "<p>Schnelle, hygienische Haarentfernung mit Premium-Wachs – mit der passenden Technik für die behandelte Zone.</p>",
    ),
    ("<li>láb, kar, hónalj vagy bikini vonal</li>", "<li>Bein, Arm, Achsel oder Bikinizone</li>"),
    ("<li>előkészítés és nyugtató utóápolás</li>", "<li>Vorbereitung und beruhigende Nachpflege</li>"),
    ("<li>személyre szabott időtartam a terület alapján</li>", "<li>Individuelle Dauer je nach Zone</li>"),
    (
        "<span class=\"service-panel__title\">Szemkörnyék- és szájápolás | 30 perc</span>",
        '<span class="service-panel__title">Augen- und Lippenpflege | 30 Min.</span>',
    ),
    (
        "                          Kíméletes ápolás a finom bőrfelületekre — hidratálás, frissítés és szépítés egy rövid, kellemes ülésben.\n",
        "                          Schonende Pflege für empfindliche Partien – Feuchtigkeit, Frische und Verschönerung in einer kurzen, angenehmen Sitzung.\n",
    ),
    ("Tekintsd meg kozmetikai árlistánkat!", "Sieh dir unsere Kosmetik-Preisliste an!"),
    ("href=\"arlista.html#price-kozmetika\">ÁRLISTA &gt;", 'href="arlista.html#price-kozmetika">PREISE &gt;'),
    ("<p class=\"subpage-kicker\">A szépség útja</p>", '<p class="subpage-kicker">Der Weg zur Schönheit</p>'),
    (
        "            Lapozz, jegyezz megoldásokat, valódi eredményeket képekben.\n",
        "            Blättere und entdecke echte Resultate in Bildern.\n",
    ),
    # Gallery alts Kosmetiki -> Kosmetik-Galerie
    ('alt="Kosmetiki galéria, 1. kép"', 'alt="Kosmetik-Galerie, Bild 1"'),
    ('alt="Kosmetiki galéria, 2. kép"', 'alt="Kosmetik-Galerie, Bild 2"'),
    ('alt="Kosmetiki galéria, 3. kép"', 'alt="Kosmetik-Galerie, Bild 3"'),
    ('alt="Kosmetiki galéria, 4. kép"', 'alt="Kosmetik-Galerie, Bild 4"'),
    ('alt="Kosmetiki galéria, 5. kép"', 'alt="Kosmetik-Galerie, Bild 5"'),
    ('alt="Kosmetiki galéria, 6. kép"', 'alt="Kosmetik-Galerie, Bild 6"'),
    ('alt="Kosmetiki galéria, 7. kép"', 'alt="Kosmetik-Galerie, Bild 7"'),
    ('alt="Kosmetiki galéria, 8. kép"', 'alt="Kosmetik-Galerie, Bild 8"'),
    ('alt="Kosmetiki galéria, 9. kép"', 'alt="Kosmetik-Galerie, Bild 9"'),
    ('alt="Kosmetiki galéria, 10. kép"', 'alt="Kosmetik-Galerie, Bild 10"'),
    ('alt="Kosmetiki galéria, 11. kép"', 'alt="Kosmetik-Galerie, Bild 11"'),
    ('alt="Kosmetiki galéria, 12. kép"', 'alt="Kosmetik-Galerie, Bild 12"'),
    # —— Hazirend ——
    ('<h3 class="hazirend-rules__title">Betegség</h3>', '<h3 class="hazirend-rules__title">Krankheit</h3>'),
    # —— Arlista table headers ——
    ('<h2 id="price-kozmetika-title" class="price-block__title">Kosmetik árlista</h2>', '<h2 id="price-kozmetika-title" class="price-block__title">Kosmetik — Preisliste</h2>'),
    ('class="price-table__th--group">Gyantázás</th>', 'class="price-table__th--group">Waxing</th>'),
    ('class="price-table__th--group">Pedikűr</th>', 'class="price-table__th--group">Pediküre</th>'),
    ("<td class=\"price-table__service\">Leoldás</td>", '<td class="price-table__service">Ablösen / Entfernen</td>'),
    # —— Rólam: testimonials (match index.de) ——
    (
        """                    <p class="testimonial-card__quote">
                      Korábbi rossz tapasztalatok miatt sokáig nem mertem kozmetikushoz járni, de ez az itt töltött első alkalmat követően
                      megváltozott. A bőröm minden kezelés után szint ragyog, remekül érzem magam, és Eliza segítségével sikerült kialakítanom a
                      helyes, bőrtípusomnak megfelelő arcápolási rutint. Szívből ajánlom!
                    </p>""",
        """                    <p class="testimonial-card__quote">
                        Nach schlechten Erfahrungen traute ich mich lange nicht zur Kosmetikerin – nach dem ersten Termin hier hat sich das geändert. Meine Haut strahlt nach jeder Behandlung, und mit Fatimes Hilfe habe ich die passende Pflegeroutine für meinen Hauttyp gefunden. Sehr empfehlenswert!
                    </p>""",
    ),
    (
        """                    <p class="testimonial-card__quote">
                      Eliza nagyon kedves, csupaszív kozmetikus, a kozmetika csodaszép, tiszta, hangulatos, mindig örömmel járok ide vissza.
                      Legutóbb a 10 alkalmas arcfiatalító kezelést vettem igénybe, és az eredmény magáért beszél, azóta több pozitív visszajelzést
                      is kaptam ismerőseimtől. Csak ajánlani tudom Elizát!
                    </p>""",
        """                    <p class="testimonial-card__quote">
                        Fatime ist sehr herzlich und eine Kosmetikerin mit Leib und Seele; der Salon ist wunderschön, sauber und stimmungsvoll – ich komme immer gern wieder. Zuletzt hatte ich eine 10er-Kur für Gesichtsverjüngung, das Ergebnis spricht für sich, und ich habe viele Komplimente bekommen. Absolute Empfehlung!
                    </p>""",
    ),
    (
        """                    <p class="testimonial-card__quote">
                      Diszkrét, figyelmes hozzáállás és gyönyörű, letisztult környezet. A kezelések után a bőröm sokkal egyenletesebb és
                      hidratáltabb — végre megtaláltam a számomra megfelelő szakembert.
                    </p>""",
        """                    <p class="testimonial-card__quote">
                        Diskret, aufmerksam und eine wunderschöne, klare Atmosphäre. Nach den Behandlungen ist meine Haut viel ebenmässiger und hydratisiert – endlich habe ich die richtige Expertin gefunden.
                    </p>""",
    ),
    (
        """                    <p class="testimonial-card__quote">
                      Minden alkalommal pontosan azt kapom, amit megbeszéltünk. A szempilla- és szemöldökkezelések tartósak, természetes hatásúak
                      — sokan meg is kérdezik, hol készült.
                    </p>""",
        """                    <p class="testimonial-card__quote">
                        Jedes Mal bekomme ich genau das, was wir besprochen haben. Wimpern- und Brauenbehandlungen sind haltbar und natürlich – viele fragen, wo ich war.
                    </p>""",
    ),
    (
        """                    <p class="testimonial-card__quote">
                      Nyugodt légkör, alapos konzultáció és prémium anyagok. A manikűröm hetekig szép maradt — ritka, hogy ennyire elégedett
                      legyek a végeredménnyel.
                    </p>""",
        """                    <p class="testimonial-card__quote">
                        Ruhige Atmosphäre, gründliche Beratung und Premium-Materialien. Meine Maniküre blieb wochenlang schön – selten war ich so zufrieden.
                    </p>""",
    ),
    (
        """                    <p class="testimonial-card__quote">
                      Esküvő előtt sminkpróbán voltam: türelmesen kipróbáltuk a variációkat, a nagy napon tökéletesen tartott. Meleg szívvel
                      ajánlom mindenkinek, aki fontos alkalomra készül.
                    </p>""",
        """                    <p class="testimonial-card__quote">
                        Vor der Hochzeit hatte ich ein Make-up-Probing: wir haben geduldig Varianten ausprobiert, am grossen Tag hielt alles perfekt. Sehr zu empfehlen für besondere Anlässe.
                    </p>""",
    ),
    ('alt="Referenzbild — munkáimból"', 'alt="Referenzbild aus meiner Arbeit"'),
    ("?text=Portré';", "?text=Portrait';"),
    # —— Piercing gallery alts ——
    ('alt="Piercing galéria, 1. kép"', 'alt="Piercing-Galerie, Bild 1"'),
    ('alt="Piercing galéria, 2. kép"', 'alt="Piercing-Galerie, Bild 2"'),
    ('alt="Piercing galéria, 3. kép"', 'alt="Piercing-Galerie, Bild 3"'),
    ('alt="Piercing galéria, 4. kép"', 'alt="Piercing-Galerie, Bild 4"'),
    ('alt="Piercing galéria, 5. kép"', 'alt="Piercing-Galerie, Bild 5"'),
    ('alt="Piercing galéria, 6. kép"', 'alt="Piercing-Galerie, Bild 6"'),
    ('alt="Piercing galéria, 7. kép"', 'alt="Piercing-Galerie, Bild 7"'),
    ('alt="Piercing galéria, 8. kép"', 'alt="Piercing-Galerie, Bild 8"'),
    ('alt="Piercing galéria, 9. kép"', 'alt="Piercing-Galerie, Bild 9"'),
    ('alt="Piercing galéria, 10. kép"', 'alt="Piercing-Galerie, Bild 10"'),
    ('alt="Piercing galéria, 11. kép"', 'alt="Piercing-Galerie, Bild 11"'),
    ('alt="Piercing galéria, 12. kép"', 'alt="Piercing-Galerie, Bild 12"'),
]


def main():
    repl = sorted(REPLACEMENTS_RAW, key=lambda x: -len(x[0]))
    for path in sorted(ROOT.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        orig = text
        for old, new in repl:
            text = text.replace(old, new)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print("updated", path.name)


if __name__ == "__main__":
    main()
