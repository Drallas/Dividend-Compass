# Plan: synthese als basis, eigen mix als persoonlijke laag

Doel: de voorbeeldscenario's uit de synthese worden de basis van de berekeningen en de standaardweergave. De huidige fondsen en aannames blijven bewaard, maar verhuizen naar de tab "Eigen mix". Niets wordt weggegooid.

## Uitgangspunt

De rekenmotor blijft hetzelfde. Een synthetische strategie wordt omgezet naar een lijst met "virtuele fondsen": per index een prijsgroei (totaalrendement min dividend), een dividendrendement en een TER. Die lijst gaat via de bestaande functie replaceFunds() in de motor. Daardoor hoeft de simulatie zelf niet te veranderen.

## Stap 0: backup

Kopieer de huidige prognose.html naar docs/backup/prognose-vóór-synthese.html en maak een git-tag v-vóór-synthese. Zo kan alles later worden teruggedraaid.

## Stap 1: huidige mix veiligstellen

De zes fondsen met hun gewichten, groei, dividend, TER en bron worden vastgelegd in data/eigen-mix.json, met de naam "Mijn huidige mix". Dat bestand is de bron voor de voorbeeldmix binnen de eigen mix. Bestaande opslag in de browser (sleutel dk-funds-v1) blijft werken; als iemand daar een eigen mix heeft, wordt die niet overschreven.

## Stap 2: synthese als standaard

Het tabblad Synthese wordt de standaardweergave en de basis van de berekening. Het toont de drie strategieën (defensief, gebalanceerd, agressief) en de varianten als kaarten, met een visuele verdeling per index. Per strategie zie je het verwachte totaalrendement, het dividend, de kosten en de uitkomst voor accumulerend en uitkerend. Inleg en looptijd komen uit de bestaande invoer, zodat die maar op één plek staan. Het losse invoerveld in de synthese-tab verdwijnt.

## Stap 3: eigen mix

Het tabblad Fondsen en aannames wordt hernoemd naar Eigen mix. De huidige catalogus en het zoekformulier blijven. Daarnaast komt er een lijst met voorbeeldmixen. Eerste voorbeeld: "Mijn huidige mix", alleen lezen als voorbeeld, maar je kunt het kopiëren en aanpassen. Een gebruiker kan een eigen mix maken, die actief zetten of verwijderen. Alleen de actieve mix stuurt de berekening.

## Stap 4: vormgeving

De synthese-tab moet visueler worden dan nu: kaarten, verdelingsbalken, een grafiek van het vermogen door de tijd voor beide varianten, en vergelijkingskaarten. De teksten blijven duidelijk over aannames, met het disclaimer ernaast.

## Stap 5: tests

Vier controles. De standaardstrategie geeft 7,25 procent totaal, 2,65 procent dividend en 0,245 procent TER voor defensief. De voorbeeldmix "Mijn huidige mix" geeft exact dezelfde uitkomst als de oude versie, zodat er geen regressie is. De inleg en looptijd die je in de invoer zet, komen in de synthese terecht. De offline-werking van de PWA blijft intact, en er zijn geen scriptfouten in NL, EN en ES.

## Stap 6: uitrol

Eerst de artifact bijwerken, dan de repo committen en pushen. De cachenaam in sw.js wordt omhoog gezet, zodat bestaande gebruikers de nieuwe versie krijgen.

## Beslispunten voor jou

Eén: moet de synthese standaard opstarten, of blijft de eigen mix standaard? Mijn voorstel is de synthese. Twee: wil je de drie varianten als vaste voorbeelden houden, of ook de extra indexen (Europa, opkomende markten, S&P 500) in de standaardkaarten zetten? Drie: wordt "Mijn huidige mix" zichtbaar voor bezoekers van de publieke site, of alleen lokaal? Mijn voorstel is alleen lokaal, want het is jouw persoonlijke mix.

## Risico's

Het grootste risico is dat bestaande opgeslagen eigen mixen verloren gaan. Daarom wordt de opslagsleutel niet gewijzigd en gebeurt de migratie niet destructief. Het tweede risico is dat de synthetische cijfers als echte historie worden gelezen. Daarom staat het label "aanname" bij elke weergave.
