# @name IZV 2020/2021 project part 2.
# @file analysis.py
# @author Juraj Lazúr, xlazur00
# @date 12.12.2020

from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import os


# muzete pridat libovolnou zakladni knihovnu ci knihovnu predstavenou na prednaskach
# dalsi knihovny pak na dotaz

# Ukol 1: nacteni dat
def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:

    # Overenie, či súbor existuje
    try:
        file_to_open = os.getcwd() + '/' + filename
        os.path.isfile(file_to_open)
    except FileNotFoundError:
        exit(-1)

    # Načítanie obsahu súboru
    try:
        raw_data = pd.read_pickle(file_to_open, compression="gzip")
    except ValueError:
        exit(-1)
    raw_data = pd.DataFrame(raw_data)

    # Výpis veľkosti dát pred zmenou dátových typov
    if verbose:
        used_memory = raw_data.memory_usage(index=False, deep=True).sum() / 1048576
        print("orig_size=%.1f MB" % used_memory)

    # Pretypovanie jednotlivých stĺpcov na vhodné dátové typy
    raw_data['p1'] = raw_data['p1'].astype('u8')
    raw_data['p36'] = raw_data['p36'].astype('category')
    raw_data['p2a'] = raw_data['p2a'].astype('M8[D]')
    raw_data['weekday(p2a)'] = raw_data['weekday(p2a)'].astype('category')
    raw_data['p2b'] = raw_data['p2b'].astype('u2')
    raw_data['p6'] = raw_data['p6'].astype('category')
    raw_data['p7'] = raw_data['p7'].astype('category')
    raw_data['p8'] = raw_data['p8'].astype('category')
    raw_data['p9'] = raw_data['p9'].astype('category')
    raw_data['p10'] = raw_data['p10'].astype('category')
    raw_data['p11'] = raw_data['p11'].astype('category')
    raw_data['p12'] = raw_data['p12'].astype('u2')
    raw_data['p13a'] = raw_data['p13a'].astype('u2')
    raw_data['p13b'] = raw_data['p13b'].astype('u2')
    raw_data['p13c'] = raw_data['p13c'].astype('u2')
    raw_data['p14'] = raw_data['p14'].astype('u2')
    raw_data['p15'] = raw_data['p15'].astype('category')
    raw_data['p16'] = raw_data['p16'].astype('category')
    raw_data['p17'] = raw_data['p17'].astype('category')
    raw_data['p18'] = raw_data['p18'].astype('category')
    raw_data['p19'] = raw_data['p19'].astype('category')
    raw_data['p20'] = raw_data['p20'].astype('category')
    raw_data['p21'] = raw_data['p21'].astype('category')
    raw_data['p22'] = raw_data['p22'].astype('category')
    raw_data['p23'] = raw_data['p23'].astype('category')
    raw_data['p24'] = raw_data['p24'].astype('category')
    raw_data['p27'] = raw_data['p27'].astype('category')
    raw_data['p28'] = raw_data['p28'].astype('category')
    raw_data['p34'] = raw_data['p34'].astype('u4')
    raw_data['p35'] = raw_data['p35'].astype('category')
    raw_data['p39'] = raw_data['p39'].astype('category')
    raw_data['p44'] = raw_data['p44'].astype('category')
    raw_data['p45a'] = raw_data['p45a'].astype('category')
    raw_data['p47'] = raw_data['p47'].astype('category')
    raw_data['p48a'] = raw_data['p48a'].astype('category')
    raw_data['p49'] = raw_data['p49'].astype('category')
    raw_data['p50a'] = raw_data['p50a'].astype('category')
    raw_data['p50b'] = raw_data['p50b'].astype('category')
    raw_data['p51'] = raw_data['p51'].astype('category')
    raw_data['p52'] = raw_data['p52'].astype('category')
    raw_data['p53'] = raw_data['p53'].astype('u4')
    raw_data['p55a'] = raw_data['p55a'].astype('category')
    raw_data['p57'] = raw_data['p57'].astype('category')
    raw_data['p58'] = raw_data['p58'].astype('category')
    raw_data['a'] = raw_data['a'].astype('f8')
    raw_data['b'] = raw_data['b'].astype('f8')
    raw_data['d'] = raw_data['d'].astype('f8')
    raw_data['e'] = raw_data['e'].astype('f8')
    raw_data['f'] = raw_data['f'].astype('f8')
    raw_data['g'] = raw_data['g'].astype('f8')
    raw_data['h'] = raw_data['h'].astype('category')
    raw_data['i'] = raw_data['i'].astype('category')
    raw_data['j'] = raw_data['j'].astype('category')
    raw_data['k'] = raw_data['k'].astype('category')
    raw_data['l'] = raw_data['l'].astype('category')
    raw_data['o'] = raw_data['o'].astype('category')
    raw_data['p'] = raw_data['p'].astype('category')
    raw_data['g'] = raw_data['g'].astype('category')
    raw_data['s'] = raw_data['s'].astype('category')
    raw_data['t'] = raw_data['t'].astype('category')
    raw_data['p5a'] = raw_data['p5a'].astype('category')
    raw_data['date'] = raw_data['p2a'].astype('M8[D]')

    # Výpis veľkosti dát po zmene dátových typov
    if verbose:
        used_memory = raw_data.memory_usage(index=False, deep=True).sum() / 1048576
        print("new_size=%.1f MB" % used_memory)
    # Vrátenie spracované dáta
    return raw_data


# Ukol 2: následky nehod v jednotlivých regionech
def plot_conseq(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    # Nastavenia grafu
    plt.style.use('seaborn-darkgrid')
    fig = plt.figure(figsize=(7, 12))
    axes = fig.subplots(nrows=4, ncols=1)

    # Agregujeme údaje podľa regiónov
    df['spec'] = 1
    plot_data = df.groupby('region').sum().sort_values(by='spec', ascending=False)

    # Každý podgraf má svoje dáta, ktoré mu poskytujeme
    data = ['p13a', 'p13b', 'p13c', 'spec']
    names = ["Úmrtí", "Těžce ranění", "Lehce ranění", "Celkem nehod"]

    # Vykresľovanie podgrafov
    for i in range(4):
        # Vykreslíme podgraf
        ax = plot_data[data[i]].plot.bar(ax=axes[i], width=0.8, color='#FF7F0E')
        # Nastavenie podgrafu
        ax.set_title(names[i], fontsize=14, fontweight='bold')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_ylabel('Počet', fontweight='bold')
        ax.set_xlabel('')

    # Úprava layoutu
    plt.tight_layout()
    # Graf uložíme
    fig.savefig(fig_location)

    # Graf prípadne vykreslíme
    if show_figure:
        plt.show()

    # Dataset uvedieme do pôvodného stavu
    del df['spec']
    plt.close()


# Ukol3: příčina nehody a škoda
def plot_damage(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    # Nastavenia grafu
    plt.style.use('seaborn-darkgrid')
    fig = plt.figure(figsize=(10, 12))
    axes = fig.subplots(nrows=3, ncols=2, gridspec_kw={'height_ratios': [1, 1, 0.1]})
    axes[2, 0].axis('off')
    axes[2, 1].axis('off')

    # Príprava dát pred spracovaním - unifikácia dôvodov nehody
    df['spec'] = df.p12 // 100
    bins = pd.IntervalIndex.from_tuples([(0, 50), (50, 200), (200, 500),
                                         (500, 1000), (1000, float("inf"))])

    # Vybrané kraje, ktoré budeme vizualizovať
    regions = ["VYS", "LBK", "HKK", "PLK"]
    cords = [(0, 0), (0, 1), (1, 0), (1, 1)]
    # Pre každý kraj vykreslíme podgraf
    for i in range(4):
        # Manipulácia s dátami pred vykresľovaním
        # Vyberieme si záznami konkrétneho kraja
        plot_data = df.loc[df['region'] == regions[i]][['p53', 'spec']]

        # Upravíme hmotnú škodu, aby bola v tisícoch
        plot_data.p53 = plot_data.p53.div(10)
        # Zaradíme škody do kategórií
        plot_data['p53'] = pd.cut(plot_data['p53'], bins, include_lowest=True)
        plot_data['p53'] = plot_data.p53.cat.rename_categories(["< 50", "50 - 200", "200 - 500",
                                                                "500 - 1000", "> 1000"])
        # Spočítame počet škôd v kategórií podľa typu nehody
        plot_data = plot_data.groupby(['p53', 'spec']).p53.agg('count').to_frame('num').reset_index()

        # Vykreslenie podgrafu
        ax = sns.barplot(data=plot_data, x="p53", y="num", hue="spec", ax=axes[cords[i]])
        # Úprava grafu
        ax.set(yscale="log")
        ax.set_title(regions[i], fontsize=14, fontweight='bold')
        ax.set_ylabel('Počet', fontweight='bold')
        ax.set_xlabel('Škoda [tisíc Kč]', fontweight='bold')
        ax.get_legend().remove()

    # Nastavenie globálnej legendy grafu
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, ["nezaviněná řidičem", "nepřiměřená rychlost jízdy", "nesprávně předjíždění",
                         "nedání přednosti v jízdě", "nesprávný zpúsob jízdy", "technická závada vozidla"],
               title="Příčina nehody", loc='lower center', ncol=3)

    # Úprava layoutu
    plt.tight_layout()
    # Graf uložíme
    fig.savefig(fig_location)

    # Graf prípadne vykreslíme
    if show_figure:
        plt.show()

    # Dataset uvedieme do pôvodného stavu
    del df['spec']
    plt.close()


# Ukol 4: povrch vozovky
def plot_surface(df: pd.DataFrame, fig_location: str = None,
                 show_figure: bool = False):
    # Nastavenia grafu
    plt.style.use('seaborn-darkgrid')
    fig = plt.figure(figsize=(10, 12))
    axes = fig.subplots(nrows=3, ncols=2, gridspec_kw={'height_ratios': [1, 1, 0.2]}, sharey='all')
    axes[2, 0].axis('off')
    axes[2, 1].axis('off')

    # Vybrané kraje, ktoré budeme vizualizovať
    regions = ["VYS", "LBK", "HKK", "PLK"]
    cords = [(0, 0), (0, 1), (1, 0), (1, 1)]
    # Pre každý kraj vykreslíme podgraf
    for i in range(4):
        # Manipulácia s dátami pred vykresľovaním
        # Vyberieme si záznami konkrétneho kraja
        plot_data = df.loc[df['region'] == regions[i]][['p16', 'date']]
        # Crosstab - prevod riadku p16 na stĺpce
        # Vznikne štatistika, kde je zaznamenaný počet stavov p16 pre jednotlivé dátumy v jednom riadku
        # Príklad:      0   1   2   3   4   5   6   7   8   9
        # Datum
        # 2016-02-08    0   2   5   8   15  4   80  2   5
        plot_data = pd.crosstab(plot_data.date, plot_data.p16)
        # Úprava hlavičky
        plot_data.columns = plot_data.columns.astype(str)
        plot_data.columns = ['jiný stav', 'suchý neznečištěný', 'suchý znečištěný', 'mokrý', 'bláto',
                             'náledí, ujetý sníh - posypané', 'náledí, ujetý sníh - neposypané',
                             'rozlitý olej, nafta apod.', 'souvislý sníh', 'náhlá změna stavu']
        plot_data.index = plot_data.index.to_period('M')
        # Agregácia dát - dni sú združené do mesiacov
        plot_data = plot_data.groupby(by=plot_data.index).sum()
        plot_data.index = plot_data.index.astype(str)

        # Vykreslíme podgraf
        g = sns.lineplot(data=plot_data, ax=axes[cords[i]])
        # Úprava grafu
        g.set_xticks([0, 12, 24, 36, 48, 60])
        g.set_xticklabels(['2016', '2017', '2018', '2019', '2020', '2021'])
        g.set_title(regions[i], fontsize=14, fontweight='bold')
        g.set_ylabel('Počet nehod', fontweight='bold')
        g.set_xlabel('Datum vzniku nehody', fontweight='bold')
        g.get_legend().remove()

    # Nastavenie globálnej legendy grafu
    handles, labels = g.get_legend_handles_labels()
    fig.legend(handles, labels,
               title="Stav vozovky", loc='lower center', ncol=4)

    # Úprava layoutu
    plt.tight_layout()
    # Graf uložíme
    fig.savefig(fig_location)

    # Graf prípadne vykreslíme
    if show_figure:
        plt.show()

    plt.close()


if __name__ == "__main__":
    pass
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni ¨
    # funkce.
    df = get_dataframe("accidents.pkl.gz")
    plot_conseq(df, fig_location="01_nasledky.png", show_figure=True)
    plot_damage(df, "02_priciny.png", False)
    plot_surface(df, "03_stav.png", False)
