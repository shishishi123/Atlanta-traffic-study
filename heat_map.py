import numpy as np
import pandas as pd
import folium
import webbrowser
from folium.plugins import HeatMap

posi1=pd.read_csv("crazy_data.csv")
posi2=pd.read_csv('total_data_of_georgia.csv')
lat1 = np.array(posi1["weidu"])
lon1 = np.array(posi1["jingdu"])
pop1 = np.array(posi1["AADT"],dtype=float)
max_AADT1=np.max(pop1)
num1=4384
data1 = [[lat1[i],lon1[i],pop1[i]] for i in range(num1)]


lat2 = np.array(posi2["weidu"])
lon2 = np.array(posi2["jingdu"])
pop2 = np.array(posi2["AADT"],dtype=float)
max_AADT2=np.max(pop1)
num2=25813
data2 = [[lat2[i],lon2[i],pop2[i]] for i in range(num2)]


map_osm = folium.Map(location=[33.796480,-84.394220],zoom_start=13,zoom_control=True,max_zoom=17,min_zoom=12)

map_osm2 = folium.Map(location=[33.796480,-84.394220],zoom_start=11,zoom_control=True,max_zoom=17,min_zoom=7)

map_osm.choropleth(
    geo_data=open('apd_beat.geojson').read(),
    fill_color='YlOrRd',
    fill_opacity=0.1,
    highlight=True,
    )

map_osm2.choropleth(
     geo_data=open('apd_beat.geojson').read(),
     fill_color='YlOrRd',
     fill_opacity=0.1,
     highlight=True,
    )

rad=int(map_osm.zoom_start*2.8)

HeatMap(data1,max_val=max_AADT1,radius=rad).add_to(map_osm)
HeatMap(data2,max_val=max_AADT2,radius=15).add_to(map_osm2)

file_path = "heatmap.html"
map_osm.save(file_path)
file_path2 = "heatmap2.html"
map_osm2.save(file_path2)

webbrowser.open(file_path)
webbrowser.open(file_path2)