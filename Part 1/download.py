# @name IZV 2020/2021 project part 1.
# @file download.py
# @author Juraj Lazúr, xlazur00
# @date 7.11.2020

# Importované knižnice
import os
import requests as req
import re
import zipfile
import csv
import numpy as np
import time
import pickle
import gzip


# Funkcia, ktorá na základe značky regiónu vráti jeho číselný kód,
# ktorý zodpovedá súboru s dátami pre daný región
def get_region_num(region):
    if region == "PHA":
        return "00"
    elif region == "STC":
        return "01"
    elif region == "JHC":
        return "02"
    elif region == "PLK":
        return "03"
    elif region == "KVK":
        return "19"
    elif region == "ULK":
        return "04"
    elif region == "LBK":
        return "18"
    elif region == "HKK":
        return "05"
    elif region == "PAK":
        return "17"
    elif region == "OLK":
        return "14"
    elif region == "MSK":
        return "07"
    elif region == "JHM":
        return "06"
    elif region == "ZLK":
        return "15"
    elif region == "VYS":
        return "16"
    else:
        return "-1"


# Implementácia triedy DataDownloader
class DataDownloader:

    # Inicializácia triedy
    def __init__(self, url="https://ehw.fit.vutbr.cz/izv/", folder="data", cache_filename="data_{}.pkl.gz"):
        self.url = url
        self.folder = os.getcwd() + '/' + folder + "/"
        self.cache_filename = cache_filename
        # Dátová štruktúra, ktorá uchováva dáta po spracovaní v prípade,
        # že trieda DataDownloader bola inicializovaná do premennej
        self.data = {'PHA': None, 'STC': None, 'JHC': None, 'PLK': None, 'KVK': None,
                     'ULK': None, 'LBK': None, 'HKK': None, 'PAK': None, 'OLK': None,
                     'MSK': None, 'JHM': None, 'ZLK': None, 'VYS': None}
        # Rozmedzie rokov, z ktorých sa majú dáta spracovávať
        self.start_y = 2016
        self.end_y = 2020

    def download_data(self):
        # Skontrolujeme, či existuje pomocný priečinok self.folder
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)

        # Získame obsah HTML dokumentu
        resp = req.get(self.url, headers={'User-Agent': 'me'})

        # HTML dokument prechádzame, izolujeme odkazy na .zip súbory
        for line in resp.iter_lines():
            # Získame odkazy na súbory
            links = re.findall("href=[\"\'](.*?)[\"\']", line.decode('utf8'))
            for lin in links:
                # Sťahovanie jednotlivých súborov
                if re.match("(.*?)[.]zip", lin):

                    file_name = self.folder + re.findall("[/](.*?)[.]zip", lin)[0] + ".zip"

                    # Ak už daný súbor máme stiahnutý, opäť ho nesťahujeme
                    if os.path.exists(file_name):
                        continue

                    down_file = req.get(self.url + lin, stream=True)

                    # Inak súbor stiahneme do pracovného priečinku
                    with open(file_name, 'wb') as file:
                        for chunk in down_file.iter_content(chunk_size=512 * 1024):
                            file.write(chunk)

    # Pomocná funkcia - extrahuje csv súbory pre zvolený kraj, v ktorých sa nachádzajú relevantné dáta
    # Relevantné dáta - posledný dostupný mesiac v roku, keďže dáta z predchádzajúceho mesiaca
    # sú obsiahnuté aj v tom nasledujúcom
    def find_files(self, reg_num):
        files = os.listdir(self.folder)
        files_to_open = []

        # Z každého roku sa pokúsime získať údaje za celý rok - za mesiac december
        for y in range(self.start_y, self.end_y + 1):
            file = None
            for f in files:
                if re.match("^(\D+)(" + str(y) + ")(.*?)", f):
                    file = f
                    break
            # Ak údaje za celý rok nie sú dostupné, pokúsime sa ich získať
            # za posledný mesiac v roku, kedy sú dostupné
            if file is None:
                for i in range(11, 0, -1):
                    if file is None:
                        for f in files:
                            if re.match("^(.*?)" + str(i) + "(.*?)" + str(y) + "(.*?)", f):
                                file = f
                                break
                    else:
                        break

            # Ak za daný rok dáta nemáme, preskočíme ho
            if file is None:
                continue

            # Zo súboru za daný rok vyextrahujeme súbor pre píslušný kraj
            with zipfile.ZipFile(self.folder + file, 'r') as zip_f:
                zip_f.extract(reg_num + ".csv", path=self.folder)
                zip_f.close()

            os.rename(self.folder + reg_num + ".csv", self.folder + reg_num + str(y) + ".csv")
            files_to_open.append(self.folder + reg_num + str(y) + ".csv")

        # Zoznam extrahovaných súborov vrátime, aby sme z nich mohli načítať dáta
        return files_to_open

    # Pomocná funkcia - vracia počet záznamov nehôd v csv súbore
    def count_lines(self, file):
        with open(file, encoding="windows-1250") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"', )
            row_count = sum(1 for row in reader)
            csvfile.close()
            return row_count

    def parse_region_data(self, region):
        # Získame kódové označenie kraja
        reg_num = get_region_num(region)

        # V prípade neznámeho kraja vrátime chybu
        if reg_num == "-1":
            exit(-1)

        # Stiahneme archívy so vstupnými dátami
        self.download_data()
        # Extrahujeme z nich všetky csv súbory s dátami pre daný kraj
        files_to_open = self.find_files(reg_num)
        # Celkový počet záznamov pre daný kraj
        data_num = 0
        clean_data = []

        # Spočítame záznamy vo všetkých csv súboroch
        for file in files_to_open:
            data_num += self.count_lines(file)

        # Štuktúra obsahujúca dátové typy stĺpcov spracovaných dát
        types = np.dtype(
            [('ID', 'u8'), ("typ komunikacie", 'u1'), ("cislo komunikacie", 'u4'), ("datum", 'M8[D]'), ("den", 'u1'),
             ("cas", "u2"), ("druh nehody", 'u1'), ("druh zrazky", 'u1'), ("druh prekazky", 'u1'),
             ("charakter nehody", 'u1'),
             ("zavynenie nehody", 'u1'), ("pritomny alkohol", 'u1'), ("pricina nehody", 'u2'),
             ("usmrtenych osob", 'u2'), ("tazko z. osob", 'u2'),
             ("lahko z. osob", 'u2'), ("hmotna skoda", 'u4'), ("povrch vozovky", 'u1'), ("stav vozovky", 'u1'),
             ("stav komunikace", 'u1'),
             ("poveternostne podmienky", 'u1'), ("viditelnost", 'u1'), ("rozhlad", 'u1'), ("delenie komunikacie", 'u1'),
             ("poloha nehody", 'u1'),
             ("riadenie dopravy v case nehody", 'u1'), ("m. u. prednosti v jazde", 'u1'), ("specificke objekty", 'u1'),
             ("smerove pomery", 'u1'), ("pocet zuc. vozidiel", 'u4'),
             ("miesto nehody", 'u1'), ("typ kriz. komun.", 'i2'), ("druh vozidla", 'u1'), ("znacka vozidla", 'u1'),
             ("rok vyroby", 'U2'),
             ("charakter vozidla", 'i1'), ("smyk", 'i1'), ("vozidlo po nehode", 'i1'), ("unik latok", 'i1'),
             ("vyprostovanie osob", 'i1'),
             ("smer vozidla", 'i1'), ("skoda na vozidle", 'u4'), ("kategoria vodica", 'i1'), ("stav vodica", 'i1'),
             ("vonkajsie ovplyvnenie vodica", 'i1'),
             ("GPS a", 'f8'), ("GPS b", 'f8'), ("GPS d", 'f8'), ("GPS e", 'f8'), ("GPS f", 'f8'),
             ("GPS g", 'f8'), ("ulica a", 'U32'), ("ulica b", 'U32'), ("ulica c", 'U32'), ("typ kom. menom", 'U16'),
             ("cislo kom. menom", 'U4'), ("j", 'U8'), ("k", 'f4'), ("smer. voz. menom", 'U32'), ("typ jazdy", 'U16'),
             ("r", 'i4'), ("s", 'i4'), ("t", 'U32'), ("lokalita nehody", 'u1'), ("region", 'U3')])

        # Alokácia pamäti pre všetky stĺpce a záznamy zo všetkých súborov pre daný kraj
        for i in range(65):
            clean_data.append(np.empty(shape=(1, data_num), dtype=types[i]))

        data_num = 0

        # Načítavanie dát zo súborov a ich ukladanie
        for file in files_to_open:
            with open(file, encoding="windows-1250") as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"', )
                for row in reader:
                    for i in range(64):
                        # Ukladanie jednotlivých záznamov - jednotlivých nehôd
                        try:
                            clean_data[i][0][data_num] = row[i]
                        except ValueError:
                            clean_data[i][0][data_num] = -1
                    # Ku každému záznamu je pridaný atribút o príslušnom kraji
                    clean_data[64][0][data_num] = region
                    data_num += 1

                csvfile.close()
                os.remove(file)

        descr = []

        # Pri všetkých záznamoch je kontrolovaná správnosť časového údaju
        for i in range(clean_data[5][0].size):
            if clean_data[5][0][i] / 60 > 24 or clean_data[5][0][i] % 60 > 59:
                clean_data[5][0][i] = 0

        # Príprava popisov jednotlivých stĺpov
        for i in range(65):
            descr.append(types.base.descr[i][0])

        # Výstup funkcie - dvojice popis stĺpca a pole hodnôt v stĺpci
        # tuple(list[str], list[np.ndarray])
        return tuple((descr, clean_data))

    # Pomocná funkcia - overuje, či sú vstupné dáta
    # načítané v pämati, uložené v súbore alebo nespracované
    def prepare_data(self, region):
        # Ak sú spracované dáta načítané v pomocnej pamäti, funkcia končí
        if self.data[region] is None:
            # Ak už boli spracované a sú uložené v súbore načítame ich
            if os.path.exists(self.folder + self.cache_filename.format(region)):
                with gzip.open(self.folder + self.cache_filename.format(region), 'rb') as f:
                    self.data[region] = pickle.load(f)
                f.close()
            # Ak nie sú ani v pamäti, ani v súbore, spracujeme ich a uložíme do pamäti a súboru
            else:
                # Spracovanie dát
                self.data[region] = self.parse_region_data(region)
                with gzip.open(self.folder + self.cache_filename.format(region), 'wb') as f:
                    pickle.dump(self.data[region], f)
                f.close()

    def get_list(self, regions=None):
        data = []
        descr = []
        args = []

        # Ak nebol zadaný argument regions, spracujeme všetky kraje
        if regions is None:
            regions = ['PHA', 'STC', 'JHC', 'PLK', 'KVK', 'ULK', 'LBK', 'HKK', 'PAK', 'OLK', 'MSK', 'JHM', 'ZLK', 'VYS']

        # Pre každý kraj overíme stav spracovaných dát
        for reg in regions:
            if reg == '':
                exit(-1)
            self.prepare_data(reg)

        # Výsledné spracované dáta pre jednotlivé kraje spojíme do výsledného datasetu
        for i in range(65):
            for reg in regions:
                args.append(self.data[reg][1][i][0])
            data.append(np.concatenate(args))
            args.clear()

        # Pripravíme popis jednotlivých stĺpcov
        for i in range(65):
            descr.append(self.data[regions[0]][0][i])

        # Vrátime celý dataset
        # tuple(list[str], list[np.ndarray])
        return tuple((descr, data))


# Funkcia main v prípade spustenia z príkazovej riadky
if __name__ == "__main__":
    # Meranie času
    start_time = time.time()
    downloader = DataDownloader()
    # Spracovanie dát zo zvolených krajov
    processed_data = downloader.get_list(["ULK", "OLK", "ZLK"])

    # Výpis podrobností
    print("--- Statistika spracovanych dat ---\n")
    print("- Kraje zahrnute v datasete -")
    print("\tUstecky")
    print("\tOlomoucky")
    print("\tZlinsky\n")

    print("- Pocet zaznamov v datasete -")
    print("\t" + str(processed_data[1][0].size) + "\n")

    print("- Doba spracovania -")
    print("\t%3.3f sekund" % (time.time() - start_time))
