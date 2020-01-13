import pandas as pd
import folium


cctv_data = pd.read_csv('cctv_location.csv', encoding='cp949')
cctv_daesu = cctv_data['대수']
sum_daesu = 0
for i in range(0, 133):
    sum_daesu = sum_daesu + cctv_daesu[i]
cctv_radius = []
for i in range(0, len(cctv_data)):
    cctv_radius.append(int(cctv_data['대수'][i] * cctv_data['범위'][i]))
cctv_map = folium.Map(location=[35.276001, 128.500001], zoom_start=12, tiles='cartodbpositron')

for i in range(0, len(cctv_data)):
    folium.Circle([cctv_data['위도'][i],cctv_data['경도'][i]], radius=cctv_radius[i], color="green", fill_color="green", weight=1).add_to(cctv_map)

from folium.plugins import MousePosition
MousePosition().add_to(cctv_map)

import json
rfile = open("changwon.json", 'r', encoding='utf-8').read()
jsonData = json.loads(rfile)

folium.GeoJson(jsonData, style_function= lambda feature: {
    'fillColor': 'gray', 'fillOpacity': 0.3, 'color': 'black', 'weight':1, 'opacity':0.1}, name='창원시').add_to(cctv_map)
"""
cctv_mildo_num = [10, 42, 22, 29, 30, 38, 26, 51]
for i in cctv_mildo_num:
    folium.GeoJson(jsonData['features'][i], style_function= lambda feature: {
        'fillColor': 'blue', 'fillOpacity': 0.3, 'color': 'black', 'weight':1, 'opacity':0.1}, name=jsonData['features'][i]['properties']['name']).add_to(cctv_map)
"""
cctv_map.save('cctv_mapping.html')
