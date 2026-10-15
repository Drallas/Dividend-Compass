# Testplan Dividend Compass

Draai vóór elke merge naar main: `python3 tests/run_tests.py`. Alles moet slagen.

## Gedrag dat altijd moet kloppen

1. Profiel opslaan en laden: alle waarden komen exact terug (bedrag, inleg, looptijd, mix, scenario, herinvesteren, domicilie, landen, percentage spaarrekening, doelbedrag, doelwaarde).
2. Domicilie blijft bewaard na herladen en na "Alle invoer wissen".
3. Landen om te vergelijken blijven bewaard na "Alle invoer wissen".
4. Scenario's (profielen) blijven bewaard na "Alle invoer wissen".
5. Box 3-schuif verborgen zodra het domicilie niet Nederland is.
6. Maximaal vier landen om te vergelijken.
7. Landenlijst alfabetisch.
8. Getypt bedrag voor box 3 blijft exact na opslaan en laden.

## Regel voor nieuwe invoer

Elke nieuwe invoer die in een profiel hoort, moet ook in `captureState()` en `applyState()` staan én in de roundtrip-test in `tests/run_tests.py`. Anders vangt de test het niet.
