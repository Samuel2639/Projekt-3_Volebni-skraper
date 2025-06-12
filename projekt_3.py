"""
projekt_3.py: třetí projekt

autor: Samuel Richtermoc
email: Richt78545@mot.sps-dopravni.cz
"""
import requests
from bs4 import BeautifulSoup
import csv
import sys

obec_kody = []
obec_nazvy = []
voliči = []
obálky = []
platné_hlasy = []
vysledky_stran = []
strany_unikatni = set()

def ziskej_html(url_adresa):
    odpoved = requests.get(url_adresa)
    odpoved.encoding = 'utf-8'
    return BeautifulSoup(odpoved.text, 'html.parser')


def zpracuj_hlavni_stranku(url):
    soup = ziskej_html(url)
    kody = soup.find_all("td", class_="cislo")
    jmena = soup.find_all("td", class_="overflow_name")

    for k in kody:
        obec_kody.append(k.text.strip())

    for n in jmena:
        obec_nazvy.append(n.text.strip())


def zpracuj_detail_obce(kod_obce):
    detail_url = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec={kod_obce}&xvyber=2101"
    odpoved = requests.get(detail_url)

    if odpoved.status_code != 200:
        print(f"Nepodařilo se získat data pro obec {kod_obce}")
        return None

    soup = BeautifulSoup(odpoved.text, 'html.parser')

    def najdi_hodnotu(trida, headers):
        td = soup.find("td", class_=trida, headers=headers)
        return td.text.replace('\xa0', ' ') if td else "N/A"

    volici = najdi_hodnotu("cislo", "sa2")
    obalky = najdi_hodnotu("cislo", "sa5")
    platne = najdi_hodnotu("cislo", "sa6")

    hlasovani = {}

    # První tabulka stran
    nazvy_1 = soup.find_all("td", class_="overflow_name", headers="t1sa1 t1sb2")
    hlasy_1 = soup.find_all("td", class_="cislo", headers="t1sa2 t1sb3")

    # Druhá tabulka stran
    nazvy_2 = soup.find_all("td", class_="overflow_name", headers="t2sa1 t2sb2")
    hlasy_2 = soup.find_all("td", class_="cislo", headers="t2sa2 t2sb3")

    nazvy = [n.text.strip() for n in nazvy_1 + nazvy_2]
    hlasy = [h.text.replace('\xa0', ' ') for h in hlasy_1 + hlasy_2]

    for i in range(len(nazvy)):
        jmeno = nazvy[i]
        hlasu = hlasy[i] if i < len(hlasy) else "0"
        hlasovani[jmeno] = hlasu
        strany_unikatni.add(jmeno)

    return volici, obalky, platne, hlasovani


def uloz_csv(soubor):
    sloupce = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]
    sloupce += sorted(strany_unikatni)

    with open(soubor, mode='w', newline='', encoding='utf-8') as vystup:
        zapisovac = csv.DictWriter(vystup, fieldnames=sloupce, restval="0")
        zapisovac.writeheader()

        for i in range(len(obec_kody)):
            radek = {
                "Kód obce": obec_kody[i],
                "Název obce": obec_nazvy[i],
                "Voliči v seznamu": voliči[i],
                "Vydané obálky": obálky[i],
                "Platné hlasy": platné_hlasy[i]
            }

            if i < len(vysledky_stran):
                radek.update(vysledky_stran[i])

            zapisovac.writerow(radek)

    print(f"\nData byla zapsána do souboru: {soubor}")


def hlavni(url, soubor_csv):
    print(f"Zpracovávám vstupní URL: {url}")
    zpracuj_hlavni_stranku(url)

    for index, kod in enumerate(obec_kody):
        print(f"{index+1}/{len(obec_kody)}: Načítám data pro obec {kod}")
        vysledek = zpracuj_detail_obce(kod)

        if vysledek:
            v, o, p, hlasovani = vysledek
            voliči.append(v)
            obálky.append(o)
            platné_hlasy.append(p)
            vysledky_stran.append(hlasovani)
        else:
            voliči.append("N/A")
            obálky.append("N/A")
            platné_hlasy.append("N/A")
            vysledky_stran.append({})

    uloz_csv(soubor_csv)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Použití: python projekt_3.py \"URL\" název_vystupu.csv")
        sys.exit(1)

    vstupni_url = sys.argv[1]
    vystupni_soubor = sys.argv[2]

    if not vystupni_soubor.endswith(".csv"):
        vystupni_soubor += ".csv"

    hlavni(vstupni_url, vystupni_soubor)