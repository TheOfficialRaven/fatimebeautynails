# -*- coding: utf-8 -*-
"""Second pass: fix broken replacements + translate remaining Hungarian in root HTML only."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONSENT_BROKEN = """                <span class="contact-form__consent-text">
                  Ich habe die
                  <a href="#" class="contact-form__policy-link">Datenschutzerklärung gelesen und akzeptiere sie.</a>
                </span>"""

CONSENT_FIXED = """                <span class="contact-form__consent-text">
                  Ich habe die
                  <a href="#" class="contact-form__policy-link">Datenschutzerklärung</a> gelesen und akzeptiere sie.
                </span>"""

# (old, new) — order after sorting by len(old) descending
REPLACEMENTS_RAW = [
    ("Vorheriges Bildek", "Vorheriges Bild"),
    ("Nächstes Bildek", "Nächstes Bild"),
    ("Leistungaim", "Meine Leistungen"),
    # arlista hero
    (
        "Az alábbiakban megtekintheted szolgáltatásaim aktuális árait. Keress bizalommal, ha kérdésed merülne fel valamelyik kezeléssel kapcsolatban!",
        "Hier findest du die aktuellen Preise meiner Leistungen. Melde dich gern, wenn du Fragen zu einer Behandlung hast.",
    ),
    # index head
    ("<title>Fati — Prémium szépségápolás</title>", "<title>Fatime Beauty — Premium Beauty &amp; Pflege</title>"),
    ("Kivételes ápolás, természetes ragyogás.", "Außergewöhnliche Pflege, natürlicher Glanz."),
    (
        "Prémium szépségápolás tetőtől talpig",
        "Premium-Beauty von Kopf bis Fuß",
    ),
    (
        "A Fatime Beauty szalonban a professzionális manikűr-, pedikűr- és arckezelésektől a szempilla- és szemöldökliftingig mindent\n            megtalálsz, ami ragyogóvá tesz. Steril környezet, hipoallergén anyagok és 7+ év szakértelem garantálja a tartós, látványos\n            eredményt - foglalj időpontot, és tapasztald meg a különbséget!",
        "Im Salon Fatime Beauty findest du alles von professioneller Maniküre, Pediküre und Gesichtsbehandlung bis zu Wimpern- und Brauenlifting – für strahlendes Wohlbefinden. Steriles Umfeld, hypoallergene Materialien und über 7 Jahre Erfahrung sorgen für haltbare, sichtbare Ergebnisse – buche deinen Termin und überzeuge dich selbst!",
    ),
    (
        "Üdvözöllek, Fatime vagyok, a Fatime Beauty &amp; Nails alapítója. 2019 óta dolgozom azon, hogy a szakterületem és a\n            vendégközpontúság találkozásából valódi szépségélményt nyújtsak - legyen szó ragyogó arcbőrről, makulátlan körmökről, kellemes\n            pedikűrről vagy szálanként épített pillákról és természetes szemöldökről.",
        "Ich bin Fatime, Gründerin von Fatime Beauty &amp; Nails. Seit 2019 verbinde ich Fachkompetenz und Gastorientierung zu echten Beauty-Momenten – ob strahlende Haut, makellose Nägel, wohltuende Pediküre oder Wimpern in Einzeltechnik und natürliche Brauen.",
    ),
    (
        "Minden vendégemnek személyre szabott kezelést tervezek testközelről, amelyet a bőröd és az életmódod igényeihez igazítok.\n            Prémium anyagokkal és a legújabb technikákkal dolgozom, hogy az eredmény biztonságos, látványos és tartós legyen.",
        "Für jede Gästin plane ich eine massgeschneiderte Behandlung – abgestimmt auf deine Haut und deinen Alltag. Mit Premium-Produkten und modernsten Techniken erziele ich sichere, sichtbare und langanhaltende Resultate.",
    ),
    (
        "A szalonban nyugodt, barátságos környezetben steril eszközökkel, precíz higiéniai szabályok mellett várlak, hogy a kezelés végén\n            elégedetten, ragyogó megjelenéssel léphess ki az ajtón.",
        "Im Salon erwarte ich dich in ruhiger, freundlicher Atmosphäre, mit sterilen Instrumenten und klaren Hygienestandards – damit du nach der Behandlung zufrieden und strahlend nach Hause gehst.",
    ),
    ("Miért bízd rám szépséged?", "Warum deine Schönheit in meine Hände?"),
    ("Év szakmai tapasztalat", "Jahre Berufserfahrung"),
    ("Szakmai továbbképzung", "Fortbildungen"),
    ("Szakmai továbbképzés", "Fortbildungen"),
    ("Elégedett vendég", "zufriedene Gäste"),
    (
        "Lapozz végig eredményeimen, és lépjünk át együtt a hiteles szépség felé vezető úton.",
        "Stöbere durch meine Arbeiten – gemeinsam dem authentischen, schönen Ergebnis ein Stück näher.",
    ),
    (
        "Személyre szabott arckezelések prémium hatóanyagokkal, hogy a bőröd már az első alkalom után üdébb, feszesebb és ragyogóbb legyen.",
        "Individuelle Gesichtsbehandlungen mit Premium-Wirkstoffen – für frischere, straffere und strahlendere Haut schon nach dem ersten Besuch.",
    ),
    (
        "Tartós, patogénmentes körmök a letisztult natúrtól a luxus dizájnig, mindezt kényelmes viselettel és kifogástalan precizitással.",
        "Langlebige, hygienische Nägel – von natürlich-reduziert bis luxuriös-designt, mit angenehmem Tragegefühl und höchster Präzision.",
    ),
    (
        "Selymes, repedésmentes talpak és frissítő lábápolás egyedi Callux technikával, vegyszermentes ápolással és tökéletes kényelemért.",
        "Seidig-weiche, rissfreie Füsse und erfrischende Fusspflege mit der Callux-Methode – ohne aggressive Chemie, mit maximalem Komfort.",
    ),
    (
        "Pihekönnyű, dús pillasor hosszan tartó hatással, hogy smink nélkül is magabiztosan ragyoghass minden pillanatban.",
        "Federschichtes, volles Wimpernbild mit langanhaltendem Effekt – damit du ohne Make-up in jedem Moment strahlst.",
    ),
    (
        "Természetes ív, rendezett forma akár 6-8 hétre, hogy smink nélkül is ragyogó legyen a tekinteted.",
        "Natürlicher Schwung, gepflegte Form für bis zu 6–8 Wochen – dein Blick strahlt auch ohne Make-up.",
    ),
    (
        "Gyors, steril és precíz piercing prémium ékszerrel, részletes utókezelési útmutatóval, hogy a gyógyulás is gondtalan legyen.",
        "Schnelles, steriles und präzises Piercing mit Schmuck in Premium-Qualität und ausführlicher Nachsorge – für eine sorgenfreie Heilung.",
    ),
    (
        "A minőség mércéje: a visszatérő vendégek.",
        "Massstab für Qualität: Gäste, die wiederkommen.",
    ),
    (
        "Valódi eredmények, elégedett vendégek",
        "Echte Resultate, zufriedene Gäste",
    ),
    # testimonials DE (abbreviated names kept)
    (
        "Korábbi rossz tapasztalatok miatt sokáig nem mertem kozmetikushoz járni, de ez az itt töltött első alkalmat követően\n                        megváltozott. A bőröm minden kezelés után szint ragyog, remekül érzem magam, és Eliza segítségével sikerült kialakítanom a\n                        helyes, bőrtípusomnak megfelelő arcápolási rutint. Szívből ajánlom!",
        "Nach schlechten Erfahrungen traute ich mich lange nicht zur Kosmetikerin – nach dem ersten Termin hier hat sich das geändert. Meine Haut strahlt nach jeder Behandlung, und mit Fatimes Hilfe habe ich die passende Pflegeroutine für meinen Hauttyp gefunden. Sehr empfehlenswert!",
    ),
    (
        "Eliza nagyon kedves, csupaszív kozmetikus, a kozmetika csodaszép, tiszta, hangulatos, mindig örömmel járok ide vissza.\n                        Legutóbb a 10 alkalmas arcfiatalító kezelést vettem igénybe, és az eredmény magáért beszél, azóta több pozitív visszajelzést\n                        is kaptam ismerőseimtől. Csak ajánlani tudom Elizát!",
        "Fatime ist sehr herzlich und eine Kosmetikerin mit Leib und Seele; der Salon ist wunderschön, sauber und stimmungsvoll – ich komme immer gern wieder. Zuletzt hatte ich eine 10er-Kur für Gesichtsverjüngung, das Ergebnis spricht für sich, und ich habe viele Komplimente bekommen. Absolute Empfehlung!",
    ),
    (
        "Diszkrét, figyelmes hozzáállás és gyönyörű, letisztult környezet. A kezelések után a bőröm sokkal egyenletesebb és\n                        hidratáltabb — végre megtaláltam a számomra megfelelő szakembert.",
        "Diskret, aufmerksam und eine wunderschöne, klare Atmosphäre. Nach den Behandlungen ist meine Haut viel ebenmässiger und hydratisiert – endlich habe ich die richtige Expertin gefunden.",
    ),
    (
        "Minden alkalommal pontosan azt kapom, amit megbeszéltünk. A szempilla- és szemöldökkezelések tartósak, természetes hatásúak\n                        — sokan meg is kérdezik, hol készült.",
        "Jedes Mal bekomme ich genau das, was wir besprochen haben. Wimpern- und Brauenbehandlungen sind haltbar und natürlich – viele fragen, wo ich war.",
    ),
    (
        "Nyugodt légkör, alapos konzultáció és prémium anyagok. A manikűröm hetekig szép maradt — ritka, hogy ennyire elégedett\n                        legyek a végeredménnyel.",
        "Ruhige Atmosphäre, gründliche Beratung und Premium-Materialien. Meine Maniküre blieb wochenlang schön – selten war ich so zufrieden.",
    ),
    (
        "Esküvő előtt sminkpróbán voltam: türelmesen kipróbáltuk a variációkat, a nagy napon tökéletesen tartott. Meleg szívvel\n                        ajánlom mindenkinek, aki fontos alkalomra készül.",
        "Vor der Hochzeit hatte ich ein Make-up-Probing: wir haben geduldig Varianten ausprobiert, am grossen Tag hielt alles perfekt. Sehr zu empfehlen für besondere Anlässe.",
    ),
    ("1. vélemény", "1. Stimme"),
    ("2. vélemény", "2. Stimme"),
    ("3. vélemény", "3. Stimme"),
    ("4. vélemény", "4. Stimme"),
    ("5. vélemény", "5. Stimme"),
    ("6. vélemény", "6. Stimme"),
    ("1. oldal (Fruzsi, Magdi)", "1. Seite (Fruzsi, Magdi)"),
    ("2. oldal (Eszter, Judit)", "2. Seite (Eszter, Judit)"),
    ("3. oldal (Réka, Zsófi)", "3. Seite (Réka, Zsófi)"),
    (
        "A szépséged a hivatásom",
        "Deine Schönheit ist meine Berufung",
    ),
    (
        "A célom, hogy minden alkalom után magabiztosabban és elégedetten lépj ki a szalonból. Itt figyelmet, minőséget és rád szabott megoldásokat kapsz. \n          Hiszem, hogy a szépségápolás nem csak a külsőről szól – minden kezelésnél arra törekszem, hogy egy kis pluszt adjak a napodhoz, és mosollyal az arcodon távozz.",
        "Mein Ziel: Nach jedem Besuch verlässt du den Salon selbstbewusster und zufriedener. Hier bekommst du Aufmerksamkeit, Qualität und massgeschneiderte Lösungen. Beauty geht für mich nicht nur um das Äussere – bei jeder Behandlung möchte ich deinem Tag etwas Gutes geben, damit du mit einem Lächeln gehst.",
    ),
    # FAQ index + shared
    (
        "Hogyan válasszam ki a legjobb szolgáltatást, ha nem vagyok biztos benne, melyik kezelésre van szükségem?",
        "Wie wähle ich die passende Leistung, wenn ich unsicher bin, welche Behandlung ich brauche?",
    ),
    (
        "Előzetes konzultáción átbeszéljük az igényeidet és a bőröd / állapotod alapján javaslok kezeléseket. Nyugodtan hozz\n                      példákat vagy kérdéseket — együtt találjuk meg a számodra legjobb megoldást.",
        "In einem Vorgespräch klären wir deine Wünsche; je nach Haut und Befund schlage ich Behandlungen vor. Bring ruhig Beispiele oder Fragen mit – gemeinsam finden wir die beste Lösung.",
    ),
    ("Hogyan tudok időpontot foglalni?", "Wie kann ich einen Termin buchen?"),
    (
        "Írj az űrlapon, közösségi média üzenetben vagy telefonon — hamarosan visszajelzek, és egyeztetünk egy neked megfelelő\n                      időpontot.",
        "Schreib über das Formular, per Social Media oder telefonisch – ich melde mich bald und wir finden einen passenden Termin.",
    ),
    ("Van garancia?", "Gibt es eine Garantie?"),
    (
        "Meghatározott kezeléseknél 1 héten belül jelezd, ha nem vagy elégedett — megbeszéljük az esetet, és a protokollnak\n                      megfelelően keresünk megoldást.",
        "Bei bestimmten Behandlungen melde dich innerhalb einer Woche, wenn du unzufrieden bist – wir besprechen den Fall und finden gemäss Protokoll eine Lösung.",
    ),
    (
        "Mi van, ha allergiás reakcióm lenne a használt anyagokra?",
        "Was ist, wenn ich auf verwendete Produkte allergisch reagiere?",
    ),
    (
        "Kérlek mindig jelezd előre az ismert allergiákat. Szükség esetén próbakezeléssel vagy más termékkel dolgozunk — a biztonság\n                      az első.",
        "Bitte teile bekannte Allergien immer im Voraus mit. Bei Bedarf arbeiten wir mit einem Test oder anderen Produkten – Sicherheit steht an erster Stelle.",
    ),
    (
        "A szalon közelében vendégparkolási lehetőség érhető el — a pontos információt foglaláskor vagy a kapcsolat szekcióban találod.",
        "In der Nähe des Salons gibt es Gastparkplätze – genaue Infos erhältst du bei der Buchung oder im Kontaktbereich.",
    ),
    ("Milyen fizetési lehetőségek vannak?", "Welche Zahlungsmöglichkeiten gibt es?"),
    (
        "Fizethetsz készpénzzel és bankkártyával is — részletek egyeztetéskor, szükség szerint számlát állítok ki.",
        "Du kannst bar oder mit Karte zahlen – Details bei der Terminvereinbarung; auf Wunsch stelle ich eine Rechnung aus.",
    ),
    (
        "Kérdezz bátran, egyeztessünk időpontot!",
        "Frage gern nach – lass uns einen Termin finden!",
    ),
    (
        "Időpontot foglalnál vagy kérdésed van? Írj, és 24 órán belül felveszem veled a kapcsolatot.",
        "Möchtest du einen Termin oder hast du eine Frage? Schreib mir – ich melde mich innerhalb von 24 Stunden.",
    ),
    (
        "Személyre szabott kozmetikai kezelések bőrfiatalításra és problémás bőr kezelésére, modern technológiákkal és természetes\n          hatóanyagokkal.",
        "Individuelle Kosmetik für Hautverjüngung und Problemhaut – mit modernen Methoden und natürlichen Wirkstoffen.",
    ),
    ("Referenciakép", "Referenzbild"),
    ("Szakember portré", "Portrait der Expertin"),
    ("Vendégek arcápolás közben", "Gästin bei der Gesichtsbehandlung"),
    ("alt=\"Kosmetiki termékek és növényi díszítés\"", 'alt="Kosmetikprodukte und Pflanzendeko"'),
    ("Időpontot kérek &gt;", "TERMIN ANFRAGEN &gt;"),
    ("Időpontot kérek! &gt;", "TERMIN ANFRAGEN &gt;"),
    ("ÁRAINK &gt;", "PREISE &gt;"),
    # —— Pass 3: subpages + Hausordnung + Kontakt hero ——
    (
        "A házirend azért van, hogy mindenki számára kellemes, tiszteletteljes legyen a szalonban töltött idő, és az időpontok zökkenőmentesen,\n              gördülékenyen zajlanjanak. Kérlek, vedd figyelembe az alábbi pontokat — így mi is a legjobb szolgáltatást tudjuk nyújtani neked.",
        "Die Hausordnung sorgt dafür, dass sich alle Gäste im Salon wohlfühlen und Termine reibungslos ablaufen. Bitte beachte die folgenden Punkte – so kann ich dir den bestmöglichen Service bieten.",
    ),
    ('<h2 id="hazirend-rules-heading" class="visually-hidden">Szabályok</h2>', '<h2 id="hazirend-rules-heading" class="visually-hidden">Regeln</h2>'),
    (
        "Időpontot online foglalási rendszeren keresztül vagy telefonon egyeztethetünk. Kérlek, jelezd pontosan, milyen kezelésre szeretnél\n                jönni, hogy megfelelő időtartalmat tudjunk biztosítani számodra.",
        "Termine vereinbaren wir online oder telefonisch. Bitte gib genau an, welche Behandlung du wünschst, damit wir ausreichend Zeit einplanen können.",
    ),
    ("Időpont-egyeztetés", "Terminvereinbarung"),
    (
        "A többi vendég és a foglalt programok tiszteletben tartása érdekében kérlek, legfeljebb 10–15 perccel a kezdés előtt érkezz a szalonba.",
        "Bitte komm aus Rücksicht auf andere Gäste und den Zeitplan höchstens 10–15 Minuten vor Beginn des Termins.",
    ),
    ("Érkezés", "Ankunft"),
    (
        "A foglalt időpont lemondását vagy áthelyezését legalább 24 órával korábban jelezd. Későbbi lemondás vagy meg nem jelenés esetén a\n                kezelés díjának 100%-át számoljuk fel.",
        "Bitte sage Termine oder Verschiebungen mindestens 24 Stunden vorher ab. Bei kurzfristiger Absage oder Nichterscheinen wird die Behandlung zu 100 % in Rechnung gestellt.",
    ),
    ("Lemondás és késés", "Absage und Verspätung"),
    (
        "A kezelőhelyiségbe csak az adott szolgáltatást igénybe vevő vendég tartózkodhat. Kísérőket und további vendégeket a kezelőtérben nem\n                tudunk fogadni.",
        "Im Behandlungsraum darf nur die Person sein, die die Behandlung erhält. Begleitpersonen können wir im Behandlungsbereich nicht aufnehmen.",
    ),
    (
        "A kezelőhelyiségbe csak az adott szolgáltatást igénybe vevő vendég tartózkodhat. Kísérőket és további vendégeket a kezelőtérben nem\n                tudunk fogadni.",
        "Im Behandlungsraum darf nur die Person sein, die die Behandlung erhält. Begleitpersonen können wir im Behandlungsbereich nicht aufnehmen.",
    ),
    ("Vendégvonzás", "Begleitpersonen"),
    (
        "Ha betegnek érzed magad, lázad van, vagy fertőző megbetegedésre utaló tüneteid vannak, kérlek, halaszd az időpontot — saját\n                felépülésed és a többi vendég védelme érdekében.",
        "Wenn du dich krank fühlst, Fieber hast oder Anzeichen einer ansteckenden Erkrankung, verschiebe bitte den Termin – zum Schutz deiner Genesung und der anderen Gäste.",
    ),
    (
        "Biztonsági és higiéniai okokból, valamint a nyugodt kezelőkörnyezet fenntartása miatt kisállat und kísérő nélküli kisgyermek a\n                kezelőhelyiségben nem tartózkodhat.",
        "Aus Sicherheits- und Hygienegründen sowie zur ruhigen Atmosphäre dürfen im Behandlungsraum keine Haustiere und keine unbegleiteten Kleinkinder mitgebracht werden.",
    ),
    (
        "Biztonsági és higiéniai okokból, valamint a nyugodt kezelőkörnyezet fenntartása miatt kisállat és kísérő nélküli kisgyermek a\n                kezelőhelyiségben nem tartózkodhat.",
        "Aus Sicherheits- und Hygienegründen sowie zur ruhigen Atmosphäre dürfen im Behandlungsraum keine Haustiere und keine unbegleiteten Kleinkinder mitgebracht werden.",
    ),
    ("Kisállat, kisgyermek", "Haustier, Kleinkind"),
    ("IDŐPONTFOGLALÁS &gt;", "TERMIN BUCHEN &gt;"),
    (
        "Az időpontkérést üzenetben vagy<br />\n                telefonon tudod megtenni.<br />\n                Fizetési lehetőség: készpénz",
        "Terminanfragen kannst du per Nachricht oder<br />\n                telefonisch stellen.<br />\n                Zahlung: Barzahlung",
    ),
    (
        "Látványosan ívelt pillák és rendezett, természetes hatású szemöldök egy lépésben.",
        "Sichtbar geschwungene Wimpern und gepflegte, natürlich wirkende Brauen in einem Schritt.",
    ),
    (
        "A szempilla lifting egy természetes hatású emelő kezelés, amely kiemeli a saját pilláid ívét anélkül, hogy műszempillára lenne szükség.\n            Így a tekinteted már reggel ébredéskor is nyitottabb és frissebb lesz.",
        "Beim Wimpernlifting werden deine eigenen Wimpern sanft geliftet – ganz ohne künstliche Wimpern. So wirkt dein Blick schon morgens offener und frischer.",
    ),
    ("Természetes, igéző tekintet", "Natürlicher, betörender Blick"),
    ("Természetes hatás műszempilla nélkül", "Natürlicher Look ohne Wimpernverlängerung"),
    ("Íveltbb pillák, nyitottabb tekintet", "Mehr Schwung, offenerer Blick"),
    ("Tartós eredmények akár 4-6 hétig", "Haltbar bis zu 4–6 Wochen"),
    ("Kényelmes, mindennapi viselet", "Angenehm im Alltag"),
    ("Ápolt megjelenés smink nélkül is", "Gepflegt auch ohne Make-up"),
    (
        "A szemöldök laminálás segít kiemelni a természetes formát és dúsabb, rendezettebb hatást ad. A szálak egy irányba rendezhetők,\n            így az összhatás harmonikusabb és karakteresebb lesz.",
        "Beim Brauen-Lifting werden die natürliche Form und ein volleres, ordentlicheres Erscheinungsbild betont. Die Härchen lassen sich in eine Richtung legen – für ein harmonisches, ausdrucksstarkes Gesamtbild.",
    ),
    ("Kiemelt figyelem minden szálnak", "Sorgfalt für jedes Härchen"),
    ("Szemöldök laminálás", "Brauen-Lamination"),
    ("Rendezett, formázott szemöldök", "Gepflegte, geformte Brauen"),
    ("Dúsabb, teltebb hatás", "Voller wirkend"),
    ("Természetes, mégis hangsúlyos megjelenés", "Natürlich und dennoch ausdrucksstark"),
    ("Kényelmes kezelés, nincs sérülés", "Sanfte Behandlung, ohne Verletzungsrisiko"),
    ("Tartós eredmény akár 4-6 hétig is", "Haltbar bis zu 4–6 Wochen"),
    ("Tekintsd meg pedikűr árlistánkat!", "Sieh dir unsere Preisliste für Lifting &amp; Pediküre an!"),
    (
        "Szempilla lifting és szemöldök laminálás — természetes hatás, precíz kivitelezés és személyre szabott tanácsadás a ragyogó tekintetért.",
        "Wimpernlifting und Brauen-Lamination – natürlicher Look, präzise Umsetzung und persönliche Beratung für strahlende Augen.",
    ),
    ("aria-label=\"Galéria pozíció\"", 'aria-label="Galerieposition"'),
    ("Lifting galéria", "Lifting-Galerie"),
    # Piercing
    ('alt="Piercing és ékszer részlet"', 'alt="Piercing und Schmuckdetail"'),
    ("A biztonságról és önkifejezésről", "Über Sicherheit und Selbstausdruck"),
    ("Mit érdemes tudni a piercing készítésről?", "Was du über Piercings wissen solltest"),
    (
        "A piercing készítés során tiszta és biztonságos módon, nagy hangsúlyt fektetve az anyagminőségre és a precizitásra. A szalonban\n            steril körülmények között, bőrbarát fémekkel dolgozom, hogy az eredmény esztétikus és tartós legyen.",
        "Piercings setze ich sauber und sicher, mit hohen Ansprüchen an Materialqualität und Präzision. Im Salon arbeite ich unter sterilen Bedingungen mit hautfreundlichen Metallen – für ein ästhetisches, langlebiges Ergebnis.",
    ),
    ("Hipoallergén", "Hypoallergen"),
    ("Orvosi/Ni-Titán ékszerek", "Medizinischer / Ni-Titan-Schmuck"),
    ("Gyors és steril lyukasztás", "Schnelles, steriles Stechen"),
    ("Egy mozdulatos behelyezés, az ékszer azonnal a helyére kerül", "Schmuck wird in einem Schritt sofort korrekt platziert"),
    ("Akár 3 hónapos kortól", "Ab etwa 3 Monaten möglich"),
    ("Tekintsd meg piercing árlistánkat!", "Sieh dir unsere Piercing-Preisliste an!"),
    (
        "Piercing — steril környezet, minőségi ékszerek és személyre szabott tanácsadás a biztonságos beavatkozásért és a nyugodt gyógyulásért.",
        "Piercing – steriles Umfeld, hochwertiger Schmuck und persönliche Beratung für eine sichere Behandlung und entspanntes Heilen.",
    ),
    # Pilla
    (
        "A hosszabb, dúsabb, magabiztosabb tekintet a hétköznapokban is.",
        "Ein längerer, vollerer und selbstbewussterer Blick – auch im Alltag.",
    ),
    ('alt="Szempilla és szemöldök részlet, professzionális pillázás"', 'alt="Wimpern- und Brauendetail, professionelles Styling"'),
    ("A tekintetedről - ha hatásos", "Dein Blick – wenn er wirken soll"),
    ("Milyen előnyöket nyújt a műszempilla készítés?", "Welche Vorteile bietet die Wimpernverlängerung?"),
    (
        "A műszempilla készítés modern, tartós és látványos megoldás azok számára, akik szeretnék dúsabb és hangsúlyosabb pillákkal kiemelni\n            tekintetüket. A kezelések minden vendégnél egyedi hosszúságban, ívvel és sűrűségben készülnek.",
        "Die Wimpernverlängerung ist eine moderne, haltbare und eindrucksvolle Methode für einen volleren, ausdrucksstärkeren Blick. Länge, Schwung und Dichte werden individuell abgestimmt.",
    ),
    ("Dúsabb és hosszabb pillasor azonnali hatással", "Sofort vollerer, längerer Wimpernkranz"),
    ("Választható pillaívek: C,D,M,L", "Wählbare Schwünge: C, D, M, L"),
    ("Smink nélkül is hangsúlyosabb tekintet", "Ausdrucksstark auch ohne Make-up"),
    ("Tekintsd meg pilla árlistánkat!", "Sieh dir unsere Wimpern-Preisliste an!"),
    ("Über mich, munkáimról és szemléletemről", "Über mich, meine Arbeit und meine Philosophie"),
    ("Intenzív tekintet, natürlicher hatás", "Intensiver Blick, natürlicher Effekt"),
    (
        "Pillás munkáim und hangulatképek a szalonból — lapozz a nyilakkal vagy a pontokkal.",
        "Meine Wimpernarbeiten und Stimmungsbilder aus dem Salon – blättere mit Pfeilen oder Punkten.",
    ),
    # fix if Hungarian still in pilla
    (
        "Pillás munkáim és hangulatképek a szalonból — lapozz a nyilakkal vagy a pontokkal.",
        "Meine Wimpernarbeiten und Stimmungsbilder aus dem Salon – blättere mit Pfeilen oder Punkten.",
    ),
    ("Wimpern galéria", "Wimpern-Galerie"),
    (
        "Wimpern — szempilla-hosszabbítás und dúsítás természetes hatással, precíz kivitelezéssel és személyre szabott tanácsadással.",
        "Wimpern – Verlängerung und Verdichtung mit natürlichem Look, präziser Arbeit und persönlicher Beratung.",
    ),
    (
        "Wimpern — szempilla-hosszabbítás és dúsítás természetes hatással, precíz kivitelezéssel és személyre szabott tanácsadással.",
        "Wimpern – Verlängerung und Verdichtung mit natürlichem Look, präziser Arbeit und persönlicher Beratung.",
    ),
    # Callux
    ("Callux esztétikai pedikűr", "Callux-Ästhetik-Pediküre"),
    (
        "A modern esztétikai pedikűr kíméletesen ápolja lábaidat, anélkül hogy sérülést okozna.",
        "Die moderne Ästhetik-Pediküre pflegt deine Füsse schonend – ohne Verletzungen.",
    ),
    (
        "Egész, ápolt lábak minden napra",
        "Rundum gepflegte Füsse für jeden Tag",
    ),
    ("Miért jó választás a Callux esztétikai pedikűr?", "Warum Callux-Ästhetik-Pediküre?"),
    (
        "A modern esztétikai pedikűr során speciális Callux formulák és eszközök segítségével távolíthatók el a bőrkeményedések, anélkül hogy\n            vágásra vagy erős reszelésre lenne szükség.",
        "Mit speziellen Callux-Formulierungen und Instrumenten werden Hornhaut und Schwielen entfernt – ohne Schneiden oder aggressives Feilen.",
    ),
    (
        "A kezelés gyengéd, mégis hatékony, így a láb bőre bársonyosabb, simább und komfortosabb lesz már az első alkalom után.",
        "Die Behandlung ist sanft und dennoch wirksam – die Haut an den Füssen wird schon nach dem ersten Mal weicher, glatter und angenehmer.",
    ),
    (
        "A kezelés gyengéd, mégis hatékony, így a láb bőre bársonyosabb, simább és komfortosabb lesz már az első alkalom után.",
        "Die Behandlung ist sanft und dennoch wirksam – die Haut an den Füssen wird schon nach dem ersten Mal weicher, glatter und angenehmer.",
    ),
    ("Vágásmentes | Sérülés nélküli eljárung", "Ohne Schneiden | ohne Verletzung"),
    ("Vágásmentes | Sérülés nélküli eljárás", "Ohne Schneiden | ohne Verletzung"),
    ("Fájdalommentes | Magas hatékonyságú kezelés", "Schmerzfrei | hocheffektive Behandlung"),
    ("Kíméletes gyulladáscsökkentő hatásmechanizmus", "Sanfter, entzündungshemmender Ansatz"),
    ("Cukorbetegeknek, érzékeny láb esetén is ideális", "Ideal auch bei Diabetes und empfindlichen Füssen"),
    ("Akár 3-5 héten át tartó puhaság", "Bis zu 3–5 Wochen spürbar weich"),
    ("Tekintsd meg esztétikai pedikűr árlistánkat!", "Sieh dir unsere Pediküre-Preisliste an!"),
    ("Szép, ápolt lábak", "Schöne, gepflegte Füsse"),
    ("Tekintsd meg referenciamunkáim", "Sieh dir meine Referenzen an"),
    ("Ápolt, igényes megjelenés - valódi eredmények képekben.", "Gepflegter Auftritt – echte Resultate in Bildern."),
    ("Pedikűr galéria", "Pediküre-Galerie"),
    ('alt="Ápolt lábujjak, pedikűr részlet"', 'alt="Gepflegte Zehen, Pediküre-Detail"'),
    # Manikür
    ("Miért jó választás a manikűr vagy a műköröm?", "Warum Maniküre oder Nagelmodellage?"),
    (
        "A manikűr alapja minden ápolt megjelenésnek, amely biztosítja az ápolt, rendezett és tartósan szép körmöket. A zselés lakkok és műkörmök\n            évek óta a legnépszerűbb választások tartósságuk, fényük és komfortos viseletük miatt.",
        "Maniküre ist die Basis für gepflegte Hände – ordentliche, dauerhaft schöne Nägel. Gel-Lack und Modellage sind beliebt wegen Haltbarkeit, Glanz und Tragekomfort.",
    ),
    (
        "során minden részletre figyelek, legyen szó hétköznapi viseletről vagy alkalmi, látványos megjelenésről.",
        "dabei achte ich auf jedes Detail – ob Alltag oder besonderer Anlass.",
    ),
    ("Tartós, akár 3-4 hétig megőrzi szépségét", "Hält die Schönheit bis zu 3–4 Wochen"),
    ("Akril: extra erős tartás, formázható hosszabb körmökhöz", "Acryl: extra haltbar, formbar für längere Nägel"),
    ("Ideális igényes, töredező körmökre is", "Ideal auch für brüchige Nägel"),
    ("Épített műköröm", "Modellierte Nägel"),
    (
        "Finom, természetes hatás: a köröm és a bőr kíméletes ápolása, egészséges fény und ápolt megjelenés — minimális anyaghasználattal, a\n            hosszú távú körömállapotot szem előtt tartva.",
        "Sanft und natürlich: schonende Pflege von Nagel und Haut, gesunder Glanz – mit minimalem Materialverbrauch und Fokus auf langfristige Nagelgesundheit.",
    ),
    (
        "Finom, természetes hatás: a köröm és a bőr kíméletes ápolása, egészséges fény és ápolt megjelenés — minimális anyaghasználattal, a\n            hosszú távú körömállapotot szem előtt tartva.",
        "Sanft und natürlich: schonende Pflege von Nagel und Haut, gesunder Glanz – mit minimalem Materialverbrauch und Fokus auf langfristige Nagelgesundheit.",
    ),
    ("Tradicionális japán manikűr", "Traditionelle japanische Maniküre"),
    (
        "Formázás, bőrápolás és igény szerint lakkozás vagy természetes finish. Alap a mindennapos, ápolt megjelenéshez — gyorsan, higiénikusan,\n            a kezed komfortját szem előtt tartva.",
        "Formen, Hautpflege und auf Wunsch Lack oder natürlicher Finish – schnell und hygienisch, mit Komfort für deine Hände.",
    ),
    ("Manikűr galéria", "Maniküre-Galerie"),
    (
        "Manikűr, gél lakk és műköröm — precíz kivitelezés, steril környezet und személyre szabott tanácsadás, hogy a kezeid mindig ápoltak legyenek.",
        "Maniküre, Gel-Lack und Modellage – präzise Arbeit, steriles Umfeld und persönliche Beratung für immer gepflegte Hände.",
    ),
    (
        "Manikűr, gél lakk és műköröm — precíz kivitelezés, steril környezet és személyre szabott tanácsadás, hogy a kezeid mindig ápoltak legyenek.",
        "Maniküre, Gel-Lack und Modellage – präzise Arbeit, steriles Umfeld und persönliche Beratung für immer gepflegte Hände.",
    ),
    ('alt="Ápolt köröm, manikűr részlet"', 'alt="Gepflegter Nagel, Maniküre-Detail"'),
    ('alt="Épített műköröm — kész körmök"', 'alt="Modellierte Nägel — fertige Nägel"'),
    ('alt="Természetes japán manikűr"', 'alt="Natürliche japanische Maniküre"'),
    ('alt="Klasszikus manikűr"', 'alt="Klassische Maniküre"'),
    # Kozmetikai (hero + key blocks)
    ("Személyre szabott kozmetikai kezelések, hogy újra ragyoghass.", "Individuelle Kosmetik, damit du wieder strahlst."),
    ("Tudatos bőrápolás látható eredményekért", "Bewusste Hautpflege mit sichtbaren Resultaten"),
    (
        "A kozmetikai kezeléseim azoknak szólnak, akik tartósan szeretnének egészséges, nyugodt, rugalmas bőrt - akár bőrproblémákkal\n            küzdenek, akár az öregedés jeleit szeretnék megelőzni.",
        "Meine kosmetischen Behandlungen richten sich an alle, die langfristig gesunde, ruhige, elastische Haut wünschen – ob bei Hautproblemen oder zur Vorbeugung von Alterungszeichen.",
    ),
    (
        "A kezelések során a bőr mélytisztítása, feszesítése és regenerálása történik, míg a professzionális termékek, manuális és gépi\n            technikák kombinációjával. Legkorszerűbb hatóanyagokkal dolgozom, hogy a bőröd hosszú távon is ápolt, kiegyensúlyozott und\n            ragyogó legyen.",
        "Die Haut wird intensiv gereinigt, gestrafft und regeneriert – mit Profi-Produkten sowie manuellen und Gerätetechniken. Ich arbeite mit modernsten Wirkstoffen, damit deine Haut langfristig gepflegt, ausgeglichen und strahlend bleibt.",
    ),
    (
        "A kezelések során a bőr mélytisztítása, feszesítése és regenerálása történik, míg a professzionális termékek, manuális és gépi\n            technikák kombinációjával. Legkorszerűbb hatóanyagokkal dolgozom, hogy a bőröd hosszú távon is ápolt, kiegyensúlyozott és\n            ragyogó legyen.",
        "Die Haut wird intensiv gereinigt, gestrafft und regeneriert – mit Profi-Produkten sowie manuellen und Gerätetechniken. Ich arbeite mit modernsten Wirkstoffen, damit deine Haut langfristig gepflegt, ausgeglichen und strahlend bleibt.",
    ),
    (
        "A szolgáltatások között elérhetőek a személyre szabott tisztító, simító, ránctalanító und lifting kezelések.",
        "Im Angebot sind unter anderem individuelle Reinigungs-, Glättungs-, Anti-Aging- und Lifting-Behandlungen.",
    ),
    (
        "A szolgáltatások között elérhetőek a személyre szabott tisztító, simító, ránctalanító és lifting kezelések.",
        "Im Angebot sind unter anderem individuelle Reinigungs-, Glättungs-, Anti-Aging- und Lifting-Behandlungen.",
    ),
    ("Minden bőrtípusra", "Für alle Hauttypen"),
    ("Időpont egyeztetés", "Termin"),
    ("Diagnosztika és kezelési terv", "Diagnose und Behandlungsplan"),
    (
        "Személyre szabott arckezelések prémium hatóanyagokkal, hogy a bőröd már az első alkalom után üdébb, feszesebb és ragyogóbb legyen.",
        "Individuelle Gesichtsbehandlungen mit Premium-Wirkstoffen – für frischere, straffere Haut schon nach dem ersten Besuch.",
    ),
    (
        "Személyre szabott bőrdiagnosztikával felmérem bőröd állapotát, majd célzott kezelési tervet állítok össze a tartós eredményekért.",
        "Mit einer individuellen Hautanalyse erfasse ich den Zustand deiner Haut und erstelle einen gezielten Plan für langanhaltende Resultate.",
    ),
    (
        "Steril, nyugodt környezetben zajlik a kezelés, prémium termékekkel und korszerű technikákkal a látványos, mégis kíméletes eredményért.",
        "Die Behandlung erfolgt in steriler, ruhiger Atmosphäre mit Premium-Produkten und modernen Methoden – sichtbar und dennoch schonend.",
    ),
    (
        "Steril, nyugodt környezetben zajlik a kezelés, prémium termékekkel és korszerű technikákkal a látványos, mégis kíméletes eredményért.",
        "Die Behandlung erfolgt in steriler, ruhiger Atmosphäre mit Premium-Produkten und modernen Methoden – sichtbar und dennoch schonend.",
    ),
    (
        "Személyes, otthoni ápolási útmutatót kapsz, hogy az eredmény tartós maradjon und bőröd hosszú távon is egészségesen ragyogjon.",
        "Du erhältst eine persönliche Pflegeanleitung für zu Hause – damit das Ergebnis bleibt und deine Haut langfristig gesund strahlt.",
    ),
    (
        "Személyes, otthoni ápolási útmutatót kapsz, hogy az eredmény tartós maradjon és bőröd hosszú távon is egészségesen ragyogjon.",
        "Du erhältst eine persönliche Pflegeanleitung für zu Hause – damit das Ergebnis bleibt und deine Haut langfristig gesund strahlt.",
    ),
    ("Kozmetikai galéria", "Kosmetik-Galerie"),
    # Rólam hero + placeholders (DE)
    (
        "Ismerj meg jobban",
        "Lerne mich näher kennen",
    ),
    (
        "A Fatime Beauty mögött emberi figyelem, szakmai elkötelezettség und az a vágy áll, hogy minden vendég magabiztosan és jól érezze magát a bőrében.\n            Itt megismerhetsz engem, a munkám filozófiáját és azt, mire számíthatsz, ha hozzám foglalsz időpontot.",
        "Hinter Fatime Beauty stehen menschliche Aufmerksamkeit, fachliche Leidenschaft und der Wunsch, dass sich jede Gästin in ihrer Haut wohlfühlt. Hier lernst du mich, meine Philosophie und das kennen, was dich erwartet, wenn du bei mir buchst.",
    ),
    (
        "A Fatime Beauty mögött emberi figyelem, szakmai elkötelezettség és az a vágy áll, hogy minden vendég magabiztosan és jól érezze magát a bőrében.\n            Itt megismerhetsz engem, a munkám filozófiáját és azt, mire számíthatsz, ha hozzám foglalsz időpontot.",
        "Hinter Fatime Beauty stehen menschliche Aufmerksamkeit, fachliche Leidenschaft und der Wunsch, dass sich jede Gästin in ihrer Haut wohlfühlt. Hier lernst du mich, meine Philosophie und das kennen, was dich erwartet, wenn du bei mir buchst.",
    ),
    (
        "Helyettesítő szöveg: több éves tapasztalat, folyamatos továbbképzés und megbízható, prémium márkák használata. Minden kezelésnél a biztonság und az esztétikus eredmény az elsődleges cél.",
        "Mehrjährige Erfahrung, regelmässige Fortbildung und verlässliche Premium-Marken. Bei jeder Behandlung stehen Sicherheit und ein ästhetisches Ergebnis an erster Stelle.",
    ),
    (
        "Helyettesítő szöveg: több éves tapasztalat, folyamatos továbbképzés és megbízható, prémium márkák használata. Minden kezelésnél a biztonság és az esztétikus eredmény az elsődleges cél.",
        "Mehrjährige Erfahrung, regelmässige Fortbildung und verlässliche Premium-Marken. Bei jeder Behandlung stehen Sicherheit und ein ästhetisches Ergebnis an erster Stelle.",
    ),
    (
        "Helyettesítő szöveg: személyes hangvétel, nyugodt környezet und részletes konzultáció — így együtt találjuk meg a számodra legjobb megoldást.",
        "Persönlicher Ton, ruhiges Ambiente und ausführliche Beratung – so finden wir gemeinsam die beste Lösung für dich.",
    ),
    (
        "Helyettesítő szöveg: személyes hangvétel, nyugodt környezet és részletes konzultáció — így együtt találjuk meg a számodra legjobb megoldást.",
        "Persönlicher Ton, ruhiges Ambiente und ausführliche Beratung – so finden wir gemeinsam die beste Lösung für dich.",
    ),
    (
        "Helyettesítő szöveg: a szalon higiéniai szabályai und a vendég igényeinek figyelembevétele minden lépésben — nyugodt, biztonságos élményt kapsz.",
        "Klare Hygieneregeln und Rücksicht auf deine Bedürfnisse in jedem Schritt – für eine ruhige, sichere Erfahrung.",
    ),
    (
        "Helyettesítő szöveg: a szalon higiéniai szabályai és a vendég igényeinek figyelembevétele minden lépésben — nyugodt, biztonságos élményt kapsz.",
        "Klare Hygieneregeln und Rücksicht auf deine Bedürfnisse in jedem Schritt – für eine ruhige, sichere Erfahrung.",
    ),
    ("év szakmai tapasztalat", "Jahre Berufserfahrung"),
    ("szakmai tanúsítvány", "Zertifikate"),
    ("elégedett vendég", "zufriedene Gäste"),
    ("Tekintsd meg az árlistámat", "Sieh dir meine Preisliste an"),
    ("Van garancia? (1&nbsp;hét)", "Gibt es eine Garantie?"),
    ("aria-label=\"Kép nagyítva\"", 'aria-label="Bild vergrößert"'),
]


def main():
    repl = sorted(REPLACEMENTS_RAW, key=lambda x: -len(x[0]))
    for name in sorted(os.listdir(ROOT)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(ROOT, name)
        with open(path, "r", encoding="utf-8") as f:
            s = f.read()
        orig = s
        if CONSENT_BROKEN in s:
            s = s.replace(CONSENT_BROKEN, CONSENT_FIXED)
        for old, new in repl:
            s = s.replace(old, new)
        if s != orig:
            with open(path, "w", encoding="utf-8") as f:
                f.write(s)
            print("updated", name)


if __name__ == "__main__":
    main()
