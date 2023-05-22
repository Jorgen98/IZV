# @name IZV 2020/2021 project part 1.
# @file get_stat.py
# @author Juraj Lazúr, xlazur00
# @date 7.11.2020

# Importované knižnice
from download import DataDownloader
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os


# Implementácia funkcie plot_stat
def plot_stat(data_source, fig_location=None, show_figure=False):
    # Získame indexy, na ktorých sa nachádzajú záznam o kraji a dátume nehody
    reg_index = data_source[0].index("region")
    dat_index = data_source[0].index("datum")

    # Získame kraje, ktoré sa nachádzajú v datasete
    regs = np.unique(data_source[1][reg_index]).tolist()
    # V tejto premennej budú uložené súhrnné počty nehôd za jednotlivé roky v jednotlivých krajoch
    values = []

    # Zvolenie si rozmedzia rokov, z ktorých sa budú vykresľovať grafy.
    start_y = 2016
    end_y = 2020

    # Vytvorenie dátovej štruktúry pre ukladanie počtu nehôod za jednotlivé roky.
    for j in range(end_y + 1 - start_y):
        values.append([])
        for i in range(len(regs)):
            values[j].append(0)

    # Základné nastavenia výsledného grafu.
    fig = plt.figure(figsize=(7, 12))
    fig.suptitle("Štatistika nehodovosti v ČR", fontsize=18, fontweight='bold')
    plt.axis('off')

    # Prechádzadme vstupné dáta, počítame počty nehôd za jednotlivé kraje a ukladáme ich.
    for i in range(data_source[1][reg_index].size):
        # Rok v ktorom sa nehoda stala
        year = int(str(data_source[1][dat_index][i]).split('-')[0]) - start_y
        # Kraj, v ktorom sa nehoda stala
        # Pripočítame nehodu príslušnému kraju v príslušnom roku
        values[year][regs.index(data_source[1][reg_index][i])] += 1

    # Generovanie jednotlivých podgrafov pre každý rok
    for j in range(start_y, end_y + 1):
        if j == start_y:
            ax = fig.add_subplot(end_y - start_y + 1, 1, j - start_y + 1)
        else:
            ax = fig.add_subplot(end_y - start_y + 1, 1, j - start_y + 1, sharey=ax)
        # Na základe dát z príslunšného roku sa vygeneruje stĺpcový graf.
        ax.grid(b=None, which='major', axis='y', ls='-.', lw=0.25)
        ax.bar(regs, values[j - start_y], width=0.7, bottom=0, align='center', color='#00b2d9')
        ax.set_title(str(j), fontsize=14, fontweight='bold')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_ylabel('Počet nehôd', fontweight='bold')

        # Každý kraj získa svoje poradové miesto v počte nehôd.
        for i in range(len(regs)):
            pos = 0
            for k in range(len(regs)):
                if values[j - start_y][k] >= values[j - start_y][i]:
                    pos += 1
            ax.text(i - 0.2, values[j - start_y][i] + 1000, str(pos))

    plt.tight_layout()

    # Spracovanie argumentov
    # Argument fig_location
    if fig_location is not None:
        if not os.path.isdir(fig_location):
            os.mkdir(fig_location)
        plt.savefig(os.getcwd() + '/' + fig_location + '/' + 'res_plot.png')

    # Argument show_figure
    if show_figure is True:
        plt.show()


# Funkcia main v prípade spustenia z príkazovej riadky
if __name__ == "__main__":
    # Spracovanie argumentov
    parser = argparse.ArgumentParser(description='Plotting script')
    parser.add_argument('--fig_location', type=str, help='Where to save result graph')
    parser.add_argument('--show_figure', type=bool, help='Show result graph')
    arguments = parser.parse_args()

    # Získame vstupné dáta, ktoré chceme vizualizovať
    data_source = DataDownloader().get_list()
    # Spustíme proces vizualizácie
    plot_stat(data_source, arguments.fig_location, arguments.show_figure)
