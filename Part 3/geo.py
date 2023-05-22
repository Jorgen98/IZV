# @name IZV 2020/2021 project part 3.
# @file geo.py
# @author Juraj Lazúr, xlazur00
# @date 22.12.2020

import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
from sklearn.cluster import KMeans
import numpy as np
# muzeze pridat vlastni knihovny


def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    # Pretypovanie stĺpcov
    raw_data = df

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

    # Odstranenie inf a NaN
    raw_data = raw_data.replace([np.inf, -np.inf], np.nan).dropna()

    # Funkcia vracia GeoDataFrame
    return geopandas.GeoDataFrame(raw_data, geometry=geopandas.points_from_xy(raw_data["d"], raw_data["e"]),
                                  crs='EPSG:5514')


def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    # Nastavenia grafu
    fig = plt.figure(figsize=(18, 7))
    axes = fig.subplots(nrows=1, ncols=2)
    axes[0].axis('off')
    axes[1].axis('off')

    # Vyberieme si dáta konkrétneho kraja
    plot_data = gdf.loc[gdf['region'] == "LBK"]
    # Zmena typu súradnic, aby bolo možné pouziť knižnicu contextily
    plot_data = plot_data.to_crs('EPSG:3857')

    # Vizualizujeme dáta v obci
    ax = plot_data[plot_data["p5a"] == 1].plot(ax=axes[0], markersize=2, color="tab:red")
    ax.set_title("Nehody v LBK kraji: v obci", fontsize=14, fontweight='bold')
    # Pridáme pozadie
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Voyager)

    # Vizualizujeme dáta mimo obec
    ax = plot_data[plot_data["p5a"] == 2].plot(ax=axes[1], markersize=2, color="tab:green")
    ax.set_title("Nehody v LBK kraji: mimo obec", fontsize=14, fontweight='bold')
    # Pridáme pozadie
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Voyager)

    # Úprava layoutu
    plt.tight_layout()
    # Graf uložíme
    fig.savefig(fig_location)

    # Graf prípadne vykreslíme
    if show_figure:
        plt.show()

    plt.close()


def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    # Nastavenia grafu
    fig = plt.figure(figsize=(10, 10))
    axe = fig.subplots(nrows=1, ncols=1)
    axe.axis('off')

    # Vyberieme si dáta konkrétneho kraja
    plot_data = gdf.loc[gdf['region'] == "LBK"]
    # Zmena typu suradníc, aby bolo možne použiť knižnicu contextily
    plot_data = plot_data.to_crs('EPSG:3857')

    # Pre zaradenie dát do skupín podľa polohy je nutné si ich predpripraviť
    # Získame súradnice nehôd a ich zadelenie do tried
    a = np.array([(x, y) for x, y in zip(plot_data.geometry.x, plot_data.geometry.y)])
    cluster = KMeans(n_clusters=20, random_state=0).fit(
                     np.array([(x, y) for x, y in zip(plot_data.geometry.x, plot_data.geometry.y)]))
    result = pd.DataFrame(cluster.cluster_centers_)
    # Získame počty prvkov v triedach
    vals = [0] * 20
    for i in range(len(cluster.labels_)):
        vals[cluster.labels_[i]] += 1
    result['vals'] = vals
    # Pripravíme si dáta pre vykreslenie
    result = geopandas.GeoDataFrame(result, geometry=geopandas.points_from_xy(result[0], result[1]),
                                    crs='EPSG:3857')

    # Vykreslíme všetky nehody
    ax = plot_data[plot_data["p5a"] != 0].plot(ax=axe, markersize=1, color="k")
    ax.set_title("Nehody v LBK kraji.", fontsize=14, fontweight='bold')
    # Vykreslíme zhluky nehôd
    result.plot(column='vals', ax=axe, legend=True, markersize=result['vals'] / 3, alpha=0.75,
                legend_kwds={'label': "Počet nehod", 'orientation': "horizontal"})
    # Pridáme pozadie
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Voyager)

    # Úprava layoutu
    plt.tight_layout()
    # Graf uložíme
    fig.savefig(fig_location)

    # Graf prípadne vykreslíme
    if show_figure:
        plt.show()

    plt.close()


if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    plot_geo(gdf, "geo1.png", True)
    plot_cluster(gdf, "geo2.png", True)

