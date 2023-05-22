# @name IZV 2020/2021 project part 3.
# @file doc.py
# @author Juraj Lazúr, xlazur00
# @date 25.12.2020

from matplotlib import pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import seaborn as sns
import os
import numpy as np
from tabulate import tabulate


# Načítanie dát
def get_dataframe() -> pd.DataFrame:

    print("--- IZV Výpis dát pre doc.pdf ---\n")
    print("Načítavam dáta")

    # Overenie, či súbor existuje
    try:
        file_to_open = os.getcwd() + '/' + "accidents.pkl.gz"
        os.path.isfile(file_to_open)
    except FileNotFoundError:
        exit(-1)

    # Načítanie obsahu súboru
    try:
        raw_data = pd.read_pickle(file_to_open, compression="gzip")
    except ValueError:
        exit(-1)
    raw_data = pd.DataFrame(raw_data)
    # Budeme pracovať len s vybranými dátami
    raw_data = raw_data[['p36', 'p13a', 'p13b', 'p13c', 'p53']]

    # Pretypovanie jednotlivých stĺpcov na vhodné dátové typy
    raw_data['p36'] = raw_data['p36'].astype('category')
    raw_data['p13a'] = raw_data['p13a'].astype('u2')
    raw_data['p13b'] = raw_data['p13b'].astype('u2')
    raw_data['p13c'] = raw_data['p13c'].astype('u2')
    raw_data['p53'] = raw_data['p53'].astype('u8')

    # Odstranenie inf a NaN
    raw_data = raw_data.replace([np.inf, -np.inf], np.nan).dropna()

    # Zameriavame sa len na dáta o diaľniciach a cestách 1, 2, a 3 triedy
    raw_data['p36'] = raw_data['p36'].cat.remove_categories(['4', '5', '6', '7', '8'])

    # Agregovanie dát
    raw_data = raw_data.groupby('p36').agg({'p36': 'count', 'p13a': 'sum', 'p13b': 'sum', 'p13c': 'sum', 'p53': 'sum'})

    # Korekcia celkovej škody na milión Kč
    raw_data.p53 = raw_data.p53.div(10000)

    print("Spracovanie dát dokončené\n")

    # Vrátenie spracovaných dát
    return raw_data


# Graf
def plot(data: pd.DataFrame, show: bool = False):
    print("Generujem graf")

    # Nastavenia grafu
    plt.style.use('seaborn-darkgrid')
    fig = plt.figure(figsize=(11, 5))
    axes = fig.subplots(nrows=2, ncols=5, gridspec_kw={'height_ratios': [1, 0.1]})

    # Každý podgraf má svoje dáta, ktoré mu poskytujeme
    data_names = ['p36', 'p13a', 'p13b', 'p13c', 'p53']
    names = ["Celkový počet nehôd", "Úmrtia", "Ťažko zranení", "Ľahko zranení", "Hmotná škoda"]

    for i in range(5):
        # Vykreslíme podgraf
        g = sns.barplot(data=data, x=data.index, y=data_names[i], ax=axes[0, i])
        # Úprava grafu
        g.set_title(names[i], fontsize=14, fontweight='bold')
        g.set(xticklabels=[])
        g.set(xlabel=None)
        if i == 4:
            g.set_ylabel('Škoda [milión Kč]', fontweight='bold')
        else:
            g.set_ylabel('Počet', fontweight='bold')
        axes[1, i].axis('off')

    # Pridanie extra globálnej legendy grafu
    handles = [Patch(label='Diaľnice', color='C0'), Patch(label='Cesty 1. triedy', color='C1'),
               Patch(label='Cesty 2. triedy', color='C2'), Patch(label='Cesty 3. triedy', color='C3')]
    fig.legend(handles=handles, title="Druh komunikácie", loc='lower center', ncol=4)

    # Úprava layoutu
    plt.tight_layout()
    # Graf uložíme
    fig.savefig('fig.png')

    # Graf prípadne vykreslíme
    if show:
        plt.show()

    plt.close()
    print("Graf vygenerovaný\n")


# Pomocná funkcia pre formátovanie na percentá
def percentage(x):
    return str(x) + " %"


# Tabuľka
def table(data: pd.DataFrame):
    print("Vytváram tabuľku\n")

    # Príprava záhlavia tabuľky
    per_data = data.copy()
    head = ['', 'Počet nehôd', 'Úmrtia', 'Ťažko zranení', 'Ľahko zranení', 'Škoda [mil. Kč]']
    per_data.index = ['Diaľnice', 'Cesty 1. triedy', 'Cesty 2. triedy', 'Cesty 3. triedy']
    data_names = ['p36', 'p13a', 'p13b', 'p13c', 'p53']

    # Výpočet percent
    for i in range(5):
        per_data[data_names[i]] = per_data[data_names[i]] / per_data[data_names[i]].sum() * 100

    # Zaokrúhlenie
    per_data = per_data.round(2).applymap(percentage)

    # Výpis na STDOUT
    print("LATEX output")
    print(tabulate(per_data, headers=head, tablefmt='latex').replace('llllll', 'lrrrrr'))
    print("\nFormátovaný výstup")
    print(tabulate(per_data, headers=head, tablefmt='psql'))


# Hodnoty
def counts(data: pd.DataFrame):
    print("\nVýpočet hodnôt")

    # Výpočet celkového počtu nehôd
    acc_sum = data['p36'].sum()
    print("Celkový počet nehôd: %.0f\n" % acc_sum)

    # Priemerný počet mŕtvych pri nehodách na diaľniciach a cestách 1. triedy
    av_deads = data['p13a'][0] / data['p36'][0]
    print("Priemerný počet mŕtvych na 1 nehodu na ďiaľniciach: %.3f" % av_deads)
    av_deads = data['p13a'][1] / data['p36'][1]
    print("Priemerný počet mŕtvych na 1 nehodu na cestách 1. triedy: %.3f\n" % av_deads)

    # Priemerná škoda na 1 nehodu pri diaľniciach a cestách 1. triedy
    av_damage = data['p53'][0] * 1000000 / data['p36'][0]
    print("Priemerná škoda na 1 nehodu na ďiaľniciach: %.2f Kč" % av_damage)
    av_damage = data['p53'][1] * 1000000 / data['p36'][1]
    print("Priemerná škoda na 1 nehodu na cestách 1. triedy: %.2f Kč" % av_damage)


# Hlavná funkcia
if __name__ == "__main__":
    # Načítanie a spracovanie dát
    data = get_dataframe()
    # Graf
    plot(data, show=False)
    # Tabuľka
    table(data)
    # Výpočty hodnôt
    counts(data)
