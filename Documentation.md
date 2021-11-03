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
| Obyvatelstvo podle pětiletých věkových skupin a pohlaví v krajích a okresech | https://www.czso.cz/csu/czso/obyvatelstvo-podle-petiletych-vekovych-skupin-a-pohlavi-v-krajich-a-okresech | název kraje, počet obyvatel (agregované) |
| Obyvatelstvo podle jednotek věku a pohlaví ve správních obvodech obcí s rozšířenou působností | https://www.czso.cz/csu/czso/obyvatelstvo-podle-jednotek-veku-a-pohlavi-ve-spravnich-obvodech-obci-s-rozsirenou-pusobnosti | název obce, věková skupina, počet obyvatel |
| Zemřelí podle týdnů a věkových skupin v České republice | https://www.czso.cz/csu/czso/zemreli-podle-tydnu-a-vekovych-skupin-v-ceske-republice |  |
|  |  |  |
| COVID-19: Demografický přehled vykázaných očkování v čase | https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-demografie.csv |  |
| COVID-19: Základní přehled vykázaných očkování | https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-zakladni-prehled.csv |  |
| COVID-19: Přehled úmrtí dle hlášení krajských hygienických stanic | https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.csv |  |
| COVID-19: Epidemiologická charakteristika obcí | https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/obce.csv |  |
| COVID-19: Celkový (kumulativní) počet osob s prokázanou nákazou dle krajských hygienických stanic včetně laboratoří, počet vyléčených, počet úmrtí a provedených testů (v2) | https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv |  |
| COVID-19: Přehled hospitalizací | https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/hospitalizace.csv |  |

#### Úprava datových sad
###### COVID-19: Přehled úmrtí dle hlášení krajských hygienických stanic
Byla provedena transformace věku na intervalové hodnoty (0-14,...,85+). Následně se provedla agregace na základě data úmrtí a jednotlivých věkových intervalů. Frekvence agregace byla stanovena na dobu jednoho týdne. Výsledná data tedy vyjadřují počet covid umrtí za týden pro jednotlivé věkové kategorie po dobu pandemie.
###### Zemřelí podle týdnů a věkových skupin v České republice
Data o celkovém umrtí se zredukovala pouze na záznamy za poslední dva roky, kdy probíhá pandemie. Schéma se zredukovalo pouze na jednotlivá úmrtí za týden pro konkrétní věkové kategorie.

#### Plánované dotazy
