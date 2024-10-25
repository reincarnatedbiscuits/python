import geopandas as gpd
import pandas as pd
from shapely.geometry import box, Point
from contextily import Place
import contextily as cx
import numpy as np
from matplotlib import pyplot as plt
import rasterio
from rasterio.plot import show as rioshow

plt.rcParams["figure.dpi"] = 100 # lower image size

(lat, long, commute_time, commute_price, airbnb_price) = [(40.717581778670436, 40.754223263147104, 40.74906526786079, 40.74874546105663, 40.71152175641295, 40.76040794887222), 
(-74.04496863099418, -74.04754883099214, -73.99580270770137, -73.86421402323737, -73.95425606162935, -73.97465146167536),
(45, 45, 20, 30, 30, 0),
(5.65, 6.9, 2.9, 2.9, 2.9, 0),
(247, 311, 276, 371, 361, 0)]

njpath_stations = [[40.73277622135335, -74.06252114187738, "JournalSquare"], 
          [40.71961796027518, -74.04263356130758, "GroveStreet"],
          [40.726963810421125, -74.03387578120802, "NewportStation"],
          [40.73306592729705, -74.00709272742087, "ChristopherSt"],
          [40.73424157991558, -73.99874755987005, "9thSt"],
          [40.73750151633494, -73.99710604797576, "14thSt"],
          [40.742875086326976, -73.99301690420813, "23rdSt"],
          [40.74861621976857, -73.98850252377068, "33rdSt"]]

etrain_stations = [[40.71210970821305, -74.01016114290607, "WorldTradeCenter"],
                   [40.72185899983243, -74.00566302985045, "CanalSt"],
                   [40.72578350896348, -74.00395730817827, "SpringSt"],
                   [40.73235332234339, -74.0005168811052, "W4St/WashSq"],
                   [40.74048158299812, -74.00201446753069, "14thSt"],
                   [40.74531947427103, -73.9984834159791, "23rdSt"],
                   [40.752193880617995, -73.9934607807079, "34St/Penn"],
                   [40.75722270096791, -73.98969641106576, "42St/PABT"],
                   [40.762340510771224, -73.98603248293134, "50St"],
                   [40.762973661987196, -73.98189008356738, "53St/7Av"],
                   [40.76026881713358, -73.9754221194359, "5Av/53St"],
                   [40.75771241489931, -73.96941907251178, "LexingtonAv/53St"],
                   [40.74783063723673, -73.94596750494635, "CourtSq-23St"],
                   [40.749015748761636, -73.93712522098937, "QueensPlaza"],
                   [40.747166630206884, -73.89102699924068, "JacksonHts/Roosevelt"],
                   [40.721376659262354, -73.84467770689055, "ForestHills/71Av"],
                   [40.7184227629494, -73.83717153587662, "75Av"],
                   [40.71418314566512, -73.83107277127257, "KewGardens/UnionTpke"],
                   [40.70865756203792, -73.82031873902778, "Briarwood"],
                   [40.70240167392166, -73.8167249502428, "Jamaica/VanWyck"],
                   [40.70085404928298, -73.8078958556207, "Sutphin-Archer-JFK"],
                   [40.70224691307594, -73.80064885309852, "JamaicaCtr-Parson-Archer"]]

njpath_coords = [[x[0], x[1]] for x in njpath_stations]
etrain_coords = [[x[0], x[1]] for x in etrain_stations]
df2 = pd.DataFrame(njpath_coords, columns =['lat', 'long'])
df3 = pd.DataFrame(etrain_coords, columns =['lat', 'long'])

commute_full_price = []
for ct, cp, ap in list(zip(commute_time, commute_price, airbnb_price)):
    commute_full_price.append(str(ct) + ' mins, ' + str(cp) + ' USD each way, stay=' + str(ap) + ' USD')

lat_long = list(zip(lat, long))

df = pd.DataFrame(lat_long, columns =['lat', 'long'])
master_df = pd.concat([df, df2])
# gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['long'], df['lat']))
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['long'], df['lat']))
gdf.crs = "EPSG:4326"

njpath_gdf = gpd.GeoDataFrame(df2, geometry=gpd.points_from_xy(df2['long'], df2['lat']))
njpath_gdf.crs = "EPSG:4326"

etrain_gdf = gpd.GeoDataFrame(df3, geometry=gpd.points_from_xy(df3['long'], df3['lat']))
etrain_gdf.crs = "EPSG:4326"

fig = plt.figure(figsize=(40,25), constrained_layout=True)
gs = fig.add_gridspec(1, 2)
ax1 = fig.add_subplot(gs[0, 0])
# ax2 = fig.add_subplot(gs[0, 0])
for i, txt in enumerate(commute_full_price):
    if i < (len(commute_full_price) - 1):
        ax1.annotate(text=txt, xy=(gdf.get_coordinates().x.tolist()[i], gdf.get_coordinates().y.tolist()[i]))
    else:
        ax1.annotate(text="office", xy=(gdf.get_coordinates().x.tolist()[i], gdf.get_coordinates().y.tolist()[i]))
    # print(txt + f" lat:{lat_long[i][0]}, long:{lat_long[i][1]}")
for j, txt in enumerate(njpath_stations):
    ax1.annotate(text=njpath_stations[j][2], xy=(njpath_gdf.get_coordinates().x.tolist()[j], njpath_gdf.get_coordinates().y.tolist()[j]), color='r')
for k, txt in enumerate(etrain_stations):
    ax1.annotate(text=etrain_stations[k][2], xy=(etrain_gdf.get_coordinates().x.tolist()[k], etrain_gdf.get_coordinates().y.tolist()[k]), color='b')
# plt.show()
ax1.set_xticks([])
ax1.set_yticks([])
ax1.plot(njpath_gdf.get_coordinates().x.tolist(), njpath_gdf.get_coordinates().y.tolist(), '-rD')
ax1.plot(etrain_gdf.get_coordinates().x.tolist(), etrain_gdf.get_coordinates().y.tolist(), '-b^')
gdf.plot(ax = ax1)
cx.add_basemap(ax1, crs='epsg:4326', source=cx.providers.Esri.WorldStreetMap)
ax1.tick_params('x', labelrotation=90)
plt.show()
# newyorkcity = Place("West Village, New York", zoom=12)
# ax = newyorkcity.plot()
