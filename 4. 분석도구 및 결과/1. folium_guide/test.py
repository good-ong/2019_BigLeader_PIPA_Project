import os
import pandas as pd
import folium
from folium import plugins
import json

os.chdir("C:/Users/rbehd/PycharmProjects/Mobility/data")  # csv 있는 파일로

map_test = folium.Map(location=[35.22323, 128.60946], zoom_start=11, tiles=None)

rfile = open("sanggwon_all.geojson", 'r', encoding='utf-8').read()
jsonData = json.loads(rfile)
folium.GeoJson(jsonData, name='상권', style_function= lambda feature: {
    'fillColor': '#376091', 'fillOpacity': 0.7, 'color': 'black', 'weight':0.5}).add_to(map_test)
# 4-3-5. 마우스 포지션(위도, 경도) 찾기 기능
from folium.plugins import MousePosition
MousePosition().add_to(map_test)

map_test.save("map_test.html")