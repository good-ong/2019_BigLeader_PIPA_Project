import os
import pandas as pd
import folium
import numpy
from folium import plugins
import json

os.chdir("C:/Users/rbehd/PycharmProjects/Mobility/data")  # csv 있는 파일로

data = pd.read_csv("c1_parking_place.csv", encoding="cp949")

data_gong = data[data["주차장구분"]=="공영"]
# data_min = data[data["주차장구분"]=="민영"]
data_gong_sang = data_gong[data_gong["주차장유형"]=="노상"]
data_gong_oi = data_gong[data_gong["주차장유형"]=="노외"]
rad_gong_sang = data_gong_sang['주차구획수'].values
rad_gong_oi = data_gong_oi['주차구획수'].values
# rad_min = data_min['주차구획수'].values
data_gong_sang = data_gong_sang.reset_index(drop=True)
data_gong_oi = data_gong_oi.reset_index(drop=True)
# data_min = data_min.reset_index(drop=True)

# map_pplace = folium.Map(location=[35.22323, 128.60946], zoom_start=11, tiles='cartodbdark_matter')
map_pplace = folium.Map(location=[35.22323, 128.60946], zoom_start=11, tiles='cartodbpositron')
# map_pplace = folium.Map(location=[35.22323, 128.60946], zoom_start=11)

rfile_1 = open("changwon.json", 'r', encoding='cp949').read()
jsonData_1 = json.loads(rfile_1)
rfile_2 = open("sanggwon_all.geojson", 'r', encoding='utf-8').read()
jsonData_2 = json.loads(rfile_2)

# style_function에서 fillColor 는 안에 색깔, fillOpacity는 투명도, color는 선색깔, weight는 선 두께
folium.GeoJson(jsonData_1, name='창원시', style_function= lambda feature: {
    'fillColor': 'blue', 'fillOpacity': 0.3, 'color': 'black', 'weight':1, 'opacity':0.1}).add_to(map_pplace)
folium.GeoJson(jsonData_2, name='상권', style_function= lambda feature: {
    'fillColor': 'pink', 'fillOpacity': 0.7, 'color': 'black', 'weight':0.5}).add_to(map_pplace)

fg = folium.FeatureGroup(name="전체")  # 전체그룹 설정
g1 = plugins.FeatureGroupSubGroup(fg, '공영 노상')  # 서브그룹 틀 만들기
g2 = plugins.FeatureGroupSubGroup(fg, '공영 노외')
# g3 = plugins.FeatureGroupSubGroup(fg, '민영')
map_pplace.add_child(fg)  # 서브 그룹 맵에 넣기
map_pplace.add_child(g1)
map_pplace.add_child(g2)
# map_pplace.add_child(g3)


d_g_s_lati = data_gong_sang["위도"]
d_g_s_long = data_gong_sang["경도"]
d_g_o_lati = data_gong_oi["위도"]
d_g_o_long = data_gong_oi["경도"]
# 원 마커에서 color는 선 색깔, fill은 안에 채울지 말지, fill_color는 안에 채울 색깔 설정
for i in range(0, len(data_gong_sang)):
#    folium.Circle([d_g_s_lati[i], d_g_s_long[i]], radius=int(rad_gong_sang[i]),
#                  color="#ffc039", weight=1, fill=True, popup=int(rad_gong_sang[i])).add_to(g1)
     folium.Marker([d_g_s_lati[i], d_g_s_long[i]], icon=folium.Icon(color='red', icon='thumbs-up')).add_to(g1)
for k in range(0, len(data_gong_oi)):
#    folium.Circle([d_g_o_lati[k], d_g_o_long[k]], radius=int(rad_gong_oi[k]),
#                  color="#376091", weight=1, fill=True, popup=int(rad_gong_oi[k])).add_to(g2)
     folium.Marker([d_g_o_lati[k], d_g_o_long[k]], icon=folium.Icon(color='gray', icon='thumbs-up')).add_to(g2)
# for j in range(0, len(data_min)):
#     folium.Circle([data_min["위도"][j], data_min["경도"][j]], radius=int(rad_min[j]),
#                   color="#df5656", weight=1, fill=True, popup=int(rad_min[j])).add_to(g3)

d_g_s_o = data_gong[["위도","경도"]]

from folium.plugins import HeatMap
HeatMap(d_g_s_o, name="HeatMap").add_to(map_pplace)

folium.LayerControl(collapsed=False).add_to(map_pplace)

map_pplace.save("map_pplace.html")