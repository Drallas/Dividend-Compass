# Ontwerpregels Dividend Compass

Dit is de vaste standaard voor alle tabs. Wijkt een pagina ervan af, dan is dat een bewuste keuze en wordt die hier vastgelegd.

## Frame
- Maximale breedte 1200px, gecentreerd, zijmarge 24px (16px op mobiel).
- Elke tab begint direct met de inhoud. Geen paginakop of subregel: de tab-naam staat al in het menu.
- Verticale ruimte tussen blokken: 16px. Binnen een kaart: 16px of 20px padding.

## Lettergroottes (één schaal)
- Labels en hulptekst: 12,5px, kleur muted.
- Lopende tekst: 13–14px.
- Kaartkop: 15px, gewicht 600.
- Kerncijfer (hoofdkaart): 20px, gewicht 650.
- Tweede cijfer (kleine tegel, belasting per land): 15px, gewicht 600–650.
- Paginakop bestaat niet. Hoogste tekst op een pagina is 20px.

## Kaarten
- Eén stijl: wit (`--panel`), rand 1px `--line`, radius 14px, schaduw alleen in het licht.
- Kaarten staan naast elkaar met 12px tussenruimte (desktop), onder elkaar op mobiel.
- Tegels van het tweede niveau zijn ook wit, zonder grijze achtergrond.

## Bedieningselementen
- Elke instelling met een getal krijgt een invoerveld én een schuif, net als Startwaarden.
- Schuiven: 8px hoog, gevulde kant in `--div`, duim wit met blauwe rand.
- Labels boven het veld, altijd 12,5px muted.

## Belasting
- Kaarten per land staan bovenaan.
- Daaronder een dunne balk, in drie delen naast elkaar: landen kiezen + spaarrekening-schuif + overzicht "berekend over".
- Op mobiel staan de delen onder elkaar.

## Mobiel (max 900px en 640px)
- Eén kolom, geen horizontaal scrollen.
- Tabbalk is één regel die je opzij schuift.
- Kolommen van de jaartabel krijgen labels via `data-l`, op kaartjes.
- Grafieken worden op hun echte breedte getekend; aslabels worden uitgedund.

## Getallen
- Bedragen in euro: € 1.000, punt als duizendtal, komma als decimaal in procenten.
- Percentages op belasting zijn een deel van de winst (eindvermogen min inleg), niet van het startvermogen.

## Werkwijze
- Nieuwe ontwerpwijzigingen eerst op een aparte branch, screenshots naar Allard, pas daarna samenvoegen met main.
- Niets naar GitHub pushen zonder goedkeuring.
- Cache-versie in `sw.js` ophogen bij elke release.
