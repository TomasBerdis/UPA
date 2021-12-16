# UPA
Repozitář pro projekt do předmětu UPA (VUT FIT 2021)

## Instalace
Pred spúštaním samotných skriptov si je treba vytvoriť virtualne prostredie. V repozitáry projektu treba spustiť nasledujúci
prikaz ktorý vytvorí virtualne prostredie (aby tento príkaz fungoval je treba mať nainštalovaný package `python3.9-venv` ten sa d8 nainštalovať pomocou príkazu `sudo get-apt install python3.9-venv`)

```python3.9 -m venv .venv```

Nasledne je potrebne si virtualne prostredie aktivovať pomocou príkazu

```source .venv/bin/activate```

Nasledne je už len potrebné doinštalovať posledné knižnice ktoré sú potrebné pre spustenie skriptov.

```pip install -r requirements.txt```

## Spuštění
Před spuštením skriptu loader.py je potřebné mít spuštěný MongoDB server na localhost (port 27017)

Načtení dat do databáze:

`python ./loader.py`

Ak sú dáta načítane v databázi môžete spustiť program data_to_csv.py, ktorý extrakuje dáta z databáze do potrebných csv súborov pre jednotlivé dotazy.

```python ./data_to_csv.py```

Ak sú jednotlivé csv súbory vytvorené tak je možné spustiť skript custom_queries.py, ktorý načíta jednotlivé csv súbory a uloží a vykreslí jednotlivé grafy, upraví dáta pre dotazy skupiny C a na štandarný výstup vypíše potrebné tabuľky a intervali ktoré sú použité v dokumentacii.pdf

```python ./custom_queries.py```
