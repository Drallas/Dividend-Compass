# Dividend Compass: werkafspraken voor Claude

Lees eerst `DESIGN.md`. Dat is de ontwerpstandaard; wijk er niet van af zonder dat Allard het goedkeurt.

- Bouw in een aparte branch. Maak screenshots van de gewijzigde tabs (desktop 1280px en mobiel 390px) en stuur die, voordat er iets naar main of GitHub gaat.
- Push pas naar GitHub nadat Allard het goedkeurt.
- Ophogen van de cache-versie in `sw.js` bij elke release.
- Taal: Nederlands, tenzij Allard in een andere taal schrijft. Bedragen in euro, datum als DD-MM-JJJJ.
- Het hele front-end staat in `index.html` (HTML, CSS en JavaScript in één bestand).
- Commits eindigen met de regels `Co-Authored-By:` en `Claude-Session:` zoals gebruikelijk in dit project.

- Draai vóór elke merge naar main `python3 tests/run_tests.py`; alle tests moeten slagen. Zie TESTPLAN.md.
