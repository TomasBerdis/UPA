#UPA - 1. část

###Instalace - 
###Spuštění - 
##Zvolené téma: 03: COVID-19 
####Vybrané zdroje
#####Otevřené datové sady COVID-19 v ČR
https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19
#####Český statistický úřad
https://www.czso.cz/

####Datové sady se zdrojů: 
#####COVID-19: Základní přehled
https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-zakladni-prehled.csv

#####COVID-19: Demografický přehled vykázaných očkování v čase
https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-demografie.csv

#####Zemřelí podle týdnů a věkových skupin v České republice
https://www.czso.cz/documents/62353418/155512385/130185-21data110221.csv

#####COVID-19: Přehled úmrtí dle hlášení krajských hygienických stanic
https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.csv


####Úprava datových sad:
######COVID-19: Přehled úmrtí dle hlášení krajských hygienických stanic
+ Byla provedena transformace věku na intervalové hodnoty (0-14,...,85+). Následně se provedla agregace na základě data úmrtí a jednotlivých věkových intervalů. Frekvence agregace byla stanovena na dobu jednoho týdne. Výsledná data tedy vyjadřují počet covid umrtí za týden pro jednotlivé věkové kategorie po dobu pandemie.
######Zemřelí podle týdnů a věkových skupin v České republice
+ Data o celkovém umrtí se zredukovala pouze na záznamy za poslední dva roky, kdy probíhá pandemie. Schéma se zredukovalo pouze na jednotlivá úmrtí za týden pro konkrétní věkové kategorie.

####Plánované dotazy