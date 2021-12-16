# UPA
Repozitář pro projekt do předmětu UPA (VUT FIT 2021)

## Instalace
Před spouštěním samotných skriptů je třeba si vytvořit virtualní prostředí. V repozitáři projektu je třeba spustit následující
příkaz který vytvoří virtualní prostředí (aby tento příkaz fungoval je třeba mít nainstalovaný package `python3.9-venv` ten se dá nainstalovat pomocí příkazu `sudo apt-get install python3.9-venv`) 

```python3.9 -m venv .venv```

Následně je třeba si virtualní prostředí aktivovat pomocí příkazu 

```source .venv/bin/activate```

Následně je už jen potřeba nainstalovat knihovny, které jsou potřebné pro spuštění skriptů. 
```pip3.9 install -r requirements.txt```

## Spuštění
Před spuštením skriptu loader.py je potřebné mít spuštěný MongoDB server na localhost (port 27017)

Načtení dat do databáze:

```python3.9 ./loader.py```

Pokud jsou data načtena v databázi můžete spustit program data_to_csv.py, který extrakuje data z databáze do potřebných csv souborů pro jednotlivé dotazy. 

```python3.9 ./data_to_csv.py```

Pokud jsou jednotlivé csv soubory vytvořeny tak lze spustit skript custom_queries.py, který načte jednotlivé csv soubory a uloží, vykreslí jednotlivé grafy, upraví data pro dotazy skupiny C a na standardní výstup vypíše potřebné tabulky a intervaly které jsou použity v dokumentaci.pdf 

```python3.9 ./custom_queries.py```

Chcete-li ukončit a vypnout virtual environment stačí napsat příkaz `deactivate`.
