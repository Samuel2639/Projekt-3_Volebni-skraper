# Projekt 3 - Volebni skraper
Tento projekt slouží k automatizovanému získávání a zpracování o výsledcích voleb pomocí web scraping. Výstupem je CSV soubor obsahující přehled volebních výsledků dle jednotlivých obcí.

## Použití
Skript se spouští z příkazové řádky s následující syntaxí:
```bash
python projekt_3.py "URL" název_vystupu.csv
```

## Příklad
```bash
python projekt_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" benešov_volby17.csv
```

## Instalace knihoven
Pro běh programu je potřeba mít nainstalovány následující Python knihovny:
```bash
pip install requests beautifulsoup4
```

## Vygenerování a použití requirements.txt
Pro vytvoření souboru requirements.txt spusť v příkazovém řádku:
```bash
pip freeze > requirements.txt
```

To uloží seznam aktuálně nainstalovaných knihoven (včetně verzí).

Pokud někdo jiný bude chtít projekt spustit, může knihovny nainstalovat jednoduše tímto příkazem:
```bash
pip install -r requirements.txt
```

## Jak skript funguje
Po spuštění skript načte zadanou stránku s výsledky voleb, získá kódy všech obcí a postupně projde každou z nich. Pro každou obec si stáhne detailní informace – kolik bylo voličů, vydaných obálek, platných hlasů a kolik hlasů získala každá strana. Nakonec to všechno uloží do jednoho CSV souboru, který si pojmenujete sami.
