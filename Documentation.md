# Dokumentace 1. části projektu z předmětu UPA

### Instalace - 
### Spuštění - 
## Zvolené téma: 03: COVID-19 
#### Vybrané zdroje
- Český statistický úřad - https://www.czso.cz/
- Otevřené datové sady COVID-19 v ČR - https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19

#### Datové sady ze zdrojů
| Název | Odkaz | Atributy |
| ------ | ------ | ------ |
| Obyvatelstvo podle pětiletých věkových skupin a pohlaví v krajích a okresech | https://www.czso.cz/csu/czso/obyvatelstvo-podle-petiletych-vekovych-skupin-a-pohlavi-v-krajich-a-okresech | název kraje, počet obyvatel |
| Obyvatelstvo podle jednotek věku a pohlaví ve správních obvodech obcí s rozšířenou působností | https://www.czso.cz/csu/czso/obyvatelstvo-podle-jednotek-veku-a-pohlavi-ve-spravnich-obvodech-obci-s-rozsirenou-pusobnosti | název obce, věková skupina, počet obyvatel |
| Zemřelí podle týdnů a věkových skupin v České republice | https://www.czso.cz/csu/czso/zemreli-podle-tydnu-a-vekovych-skupin-v-ceske-republice | datum, věková skupina, počet úmrtí |
|  |  |  |
| COVID-19: Demografický přehled vykázaných očkování v čase | https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-demografie.csv | datum, název vakcíny, kód vakcíny, pořadí dávky, věková skupina, pohlaví, počet dávek |
| COVID-19: Základní přehled vykázaných očkování | https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-zakladni-prehled.csv | název kraje, kód kraje, název bydliště, kód bydliště, název vakcíny, kód vakcíny, pořadí dávky, věková skupina, pohlaví, počet dávek |
| COVID-19: Přehled úmrtí dle hlášení krajských hygienických stanic | https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.csv | datum, věková skupina, počet úmrtí |
| COVID-19: Epidemiologická charakteristika obcí | https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/obce.csv | datum, název obce, kód obce, denní přírustek nakažených |
| COVID-19: Celkový (kumulativní) počet osob s prokázanou nákazou dle krajských hygienických stanic včetně laboratoří, počet vyléčených, počet úmrtí a provedených testů (v2) | https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv | datum, počet nakažených, počet vyléčených, počet úmrtí, počet hospitalizovaných, počet AG testů, počet PCR testů |
| COVID-19: Přehled hospitalizací | https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/hospitalizace.csv | datum, počet hospitalizovaných, bezpříznakové stavy, lehké stavy, střední stavy, těžké stavy, jip, kyslík, hfno, upv, ecmo, těžký upv ecmo |

#### Úprava datových sad
###### Obyvatelstvo podle pětiletých věkových skupin a pohlaví v krajích a okresech
Z této sady jsou potřebná jenom data o krajích. Záznamy jsou vybrány pro rok 2020. Pro celkový počet obyvatel daného kraje byli vybrány všechny řádky s prázdnou hodnotou pohlaví pro daný kraj. Následně byl vybrán řádek s nejvyšší hodnotou reprezentující počet obyvatel ve všech věkových skupinách.
###### Obyvatelstvo podle jednotek věku a pohlaví ve správních obvodech obcí s rozšířenou působností
Počet obyvatel byl sečten z obou pohlaví pro každou obec a věkovou kategorii. Věk bylo potřeba převést do čitelnější podoby pomocí regexu.
###### COVID-19: Přehled úmrtí dle hlášení krajských hygienických stanic
Byla provedena transformace věku na intervalové hodnoty (0-14,...,85+). Následně se provedla agregace na základě data úmrtí a jednotlivých věkových intervalů. Frekvence agregace byla stanovena na dobu jednoho týdne. Výsledná data tedy vyjadřují počet covid umrtí za týden pro jednotlivé věkové kategorie po dobu pandemie.
###### Zemřelí podle týdnů a věkových skupin v České republice
Data o celkovém umrtí se zredukovala pouze na záznamy za poslední dva roky, kdy probíhá pandemie. Schéma se zredukovalo pouze na jednotlivá úmrtí za týden pro konkrétní věkové kategorie.

#### Plánované dotazy
