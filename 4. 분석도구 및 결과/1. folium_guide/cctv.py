import os
import pandas as pd
import folium
from folium import plugins
import json

os.chdir("C:/Users/rbehd/PycharmProjects/Mobility/data")  # csv 있는 파일로

data = pd.read_csv("c_CCTV.csv", encoding="cp949")
data['설치목적구분'].unique()

data_bangbum = data[data["설치목적구분"]=="생활방범"]
data_boho = data[data["설치목적구분"]=="어린이보호"]
data_sujib = data[data["설치목적구분"]=="교통정보수집"]
data_trash = data[data["설치목적구분"]=="쓰레기단속"]
data_jaehae = data[data["설치목적구분"]=="재난재해"]
data_dansok = data[data["설치목적구분"]=="교통단속"]
data_etc = data[data["설치목적구분"]=="기타"]

data_traffic = pd.concat([data_sujib, data_dansok]).reset_index(drop=True)
data_non_traffic = pd.concat([data_bangbum, data_boho, data_trash, data_jaehae, data_etc]).reset_index(drop=True)

map_cctv = folium.Map(location=[35.22323, 128.60946], zoom_start=11, tiles='OpenStreetMap')

rfile = open("changwon.json", 'r', encoding='cp949').read()
jsonData = json.loads(rfile)
folium.GeoJson(jsonData, name='읍면동 구분').add_to(map_cctv)

# 4-3-5. 마우스 포지션(위도, 경도) 찾기 기능
# from folium.plugins import MousePosition
# MousePosition().add_to(map_cctv)

# 4-3-6. 측정도구 기능
# from folium.plugins import MeasureControl
# map_pplace.add_child(MeasureControl())
len(data[data['카메라대수'] == 4])

fg = folium.FeatureGroup(name="cctv 전체")  # 전체그룹 설정
g1 = plugins.FeatureGroupSubGroup(fg, '교통용 cctv')  # 서브그룹 틀 만들기
g2 = plugins.FeatureGroupSubGroup(fg, '비교통용 cctv')
map_cctv.add_child(fg)  # 서브 그룹 맵에 넣기
map_cctv.add_child(g1)
map_cctv.add_child(g2)
for i in range(0, len(data_traffic)):
    folium.Circle([data_traffic["위도"][i], data_traffic["경도"][i]], radius=50, color="#ffc039", fill=True).add_to(g1)
for j in range(0, len(data_non_traffic)):
    folium.Circle([data_non_traffic["위도"][j], data_non_traffic["경도"][j]], radius=50, color="#376091", fill=True).add_to(g2)

folium.LayerControl(collapsed=False).add_to(map_cctv)

map_cctv.save("map_cctv.html")
