# folium 간단 안내서 입니다.

"""
folium이란?
지도를 활용할 수 있는 파이썬 패키지 이름입니다.

사용한 자료
- 2018.06.30 창원시 CCTV 현황.csv  (c_CCTV.csv)
- 2018.06.30 창원시 주차장 정보.csv  (c1_parking_place.csv)

잘못된 내용은 없을 겁니다. 다 직접 돌려봤습니다.
다만 추가하지 못한 내용은 많을수도 있습니다. 말 그대로 간단 안내서라..
이정도만 있으면 데이터 시각화에는 무리 없을 듯 합니다.
"""


"""
0. folium 패키지 설치
프롬프트창에 pip install folium 입력 후 엔터
"""


"""
1. 패키지 및 플러그인 라이브러리 임포트
"""
import os
import pandas as pd
import folium
from folium import plugins


"""
2. 데이터 준비 (위도 경도가 있는 '주차장 정보' 및 'cctv 정보')
"""
os.chdir("C:/Users/rbehd/PycharmProjects/Mobility/data")  # csv 있는 파일로

data_p = pd.read_csv("c1_parking_place.csv", encoding="cp949")
data_c = pd.read_csv("c_CCTV.csv", encoding="cp949")

data_p.columns  # 주차장 정보의 컬럼 확인용
data_c.columns  # cctv 정보의 컬럼 확인용


"""
3. 필요한 컬럼만 남기기
이 부분은 선택사항. 그냥 데이터프레임 줄이기 위해 사용함
원데이터를 그대로 사용하겠다면 4번 항목으로
참고로 여기부터는 DataFrame, Array, List에 대한 개념을 잘 알아야 함
"""
data_cctv = data_c[["설치목적구분", "위도", "경도"]]
data_pplace = data_p[["주차장구분", "주차장유형", "위도", "경도"]]
cctv_latitude = data_cctv["위도"]
pplace_latitude = data_pplace["위도"]
cctv_longitude = data_cctv["경도"]
pplace_longitude = data_pplace["경도"]

"""
4. folium 패키지
"""
# 4-1. 보여주고자 하는 맵의 위치 넣기
map_pplace = folium.Map(location=[35.22323, 128.60946], zoom_start=12, tiles='OpenStreetMap')
"""
    zoom_start 옵션 : 시작할 때의 지도 크기 지정. 숫자 클수록 더 넓은 범위 보여줌. 기본값 12
    tiles 옵션 : 지도를 표시할 형태를 설정할 수 있음. 기본값 OpenStreetMap. StamenTerrain, StamenToner 이 있다.
    tiles 옵션에 Cloudmade, Mapbox를 사용할 수 있는데, 이 때는 API가 필요하므로 발급받은 키 정보를 넣어야 함.
    쓰는법(속성 추가) >>> API_key='키값'
"""

# 4-2. 마커 찍기
# 이해를 돕기 위해 위도와 경도 하나씩만 찍게 했음.
folium.Marker([cctv_latitude[0], cctv_longitude[0]],
              popup="CCTV 예시", icon=folium.Icon(color='red', icon='info-sign')).add_to(map_cctv)
folium.Marker([pplace_latitude[0], pplace_longitude[0]],
              popup="주차장 예시1", icon=folium.Icon(color='#3186cc', icon='cloud')).add_to(map_pplace)
folium.CircleMarker([cctv_latitude[1], cctv_longitude[1]],
                    radius=100, color="green", fill_color="green").add_to(map_cctv)
folium.CircleMarker([pplace_latitude[1], pplace_longitude[1]],
                    popup="주차장 예시2", radius=50, color="#b2ccff", fill_color="#E5D85C").add_to(map_pplace)
"""
    마커를 찍고 나선 항상 맨 뒤에 .add_to()를 쓰자. 그래야 적용이 된다.
    a. Marker : 점 마커
     - popup : 마커의 이름 표시
     - icon : 마커의 아이콘 설정 (색상에는 색상코드표 사용 가능)
    b. CircleMarker : 원 반경 표시 마커
     - popup : 마커의 이름 표시
     - radius : 반경
     - color : 원의 테두리 색깔 (색상코드표 사용 가능)
     - fill_color : 원의 안쪽 색깔 (색상코드표 사용 가능)
"""


# 4-3. folium plugin 활용하기
"""
    참조사이트(1) : https://dailyheumsi.tistory.com/85
    참조사이트(2) : https://dailyheumsi.tistory.com/92
"""

# 4-3-1. 마커 클러스터 만들기
data = data_pplace[["위도","경도"]].values  # 위도, 경도를 array로 만들기
plugins.MarkerCluster(data).ag dd_to(map_pplace)  # 마커 클러스터 삽입

# 4-3-2. 미니맵 만들기
minimap = plugins.MiniMap()
map_cctv.add_child(minimap)

# 4-3-4. 히트맵 만들기
from folium.plugins import HeatMap
HeatMap(data.tolist()).add_to(map_pplace)

# 4-3-5. 마우스 포지션(위도, 경도) 찾기 기능
from folium.plugins import MousePosition
MousePosition().add_to(map_pplace)

# 4-3-6. 측정도구 기능
from folium.plugins import MeasureControl
map_pplace.add_child(MeasureControl())

# 4-3-7. 그림 그리기 기능 (이거 되게 자주 쓰일듯!!!!!!)
# export=True 옵션 : 내가 그린 영역을 JSON 파일로 뽑아내줌
# 주의점 : 서브그룹이 많으면 4-3-7에서의 export 기능이 안됨. 직접 돌려보면 알거임.
fg = folium.FeatureGroup(name="전체")  # 전체그룹 설정
g2 = plugins.FeatureGroupSubGroup(fg, '교통정보수집')
g1 = plugins.FeatureGroupSubGroup(fg, '교통단속')  # 서브그룹 틀 만들기
from folium.plugins import Draw
Draw(export=True).add_to(map_pplace)

# 4-3-8. 그룹 만들기
g3 = plugins.FeatureGroupSubGroup(fg, '기타')
g4 = plugins.FeatureGroupSubGroup(fg, '생활방범')
g5 = plugins.FeatureGroupSubGroup(fg, '쓰레기단속')
g6 = plugins.FeatureGroupSubGroup(fg, '어린이보호')
g7 = plugins.FeatureGroupSubGroup(fg, '재난재해')

map_cctv.add_child(fg)  # 서브 그룹 맵에 넣기
map_cctv.add_child(g1)
map_cctv.add_child(g2)
map_cctv.add_child(g3)
map_cctv.add_child(g4)
map_cctv.add_child(g5)
map_cctv.add_child(g6)
map_cctv.add_child(g7)

for i in range(0, len(data_cctv)) :  # 각 서브 그룹에 해당되는 데이터 넣기
    if data_cctv["설치목적구분"][i] == "교통단속" :
        folium.Marker([cctv_latitude[i], cctv_longitude[i]]).add_to(g1)
    elif data_cctv["설치목적구분"][i] == "교통정보수집":
        folium.Marker([cctv_latitude[i], cctv_longitude[i]]).add_to(g2)
    elif data_cctv["설치목적구분"][i] == "기타" :
        folium.Marker([cctv_latitude[i], cctv_longitude[i]]).add_to(g3)
    elif data_cctv["설치목적구분"][i] == "생활방범" :
        folium.Marker([cctv_latitude[i], cctv_longitude[i]]).add_to(g4)
    elif data_cctv["설치목적구분"][i] == "쓰레기단속" :
        folium.Marker([cctv_latitude[i], cctv_longitude[i]]).add_to(g5)
    elif data_cctv["설치목적구분"][i] == "어린이보호" :
        folium.Marker([cctv_latitude[i], cctv_longitude[i]]).add_to(g6)
    if data_cctv["설치목적구분"][i] == "재난재해" :
        folium.Marker([cctv_latitude[i], cctv_longitude[i]]).add_to(g7)

folium.LayerControl(collapsed=False).add_to(map_cctv)  # 오른쪽 위에 체크박스 넣기


"""
5. 모든 작업이 끝나면 html 파일로 저장해서 확인 가능
"""
map_pplace.save("map_pplace.html")


"""
참고. 외부의 json 파일 불러들이기
json 확장자 뿐만 아니라 geojson 확장자도 먹힌다.
"""
import json

map_exam = folium.Map(location=[35.182421, 128.552426])  # 경남대학교 박물관 중심
#
rfile = open("example.geojson", 'r', encoding='utf-8').read()
jsonData = json.loads(rfile)
folium.GeoJson(jsonData, name='json_data').add_to(map_exam)
# 사실 본인은 name 옵션이 뭔지 잘 모르겠다.
map_exam.save('map_exam.html')  # map을 html로 저장하기
"""
이걸 그대로 돌리게 되면 용량이 되게 클 것이다.
그러니 자기가 필요한 부분만 활용하도록 하자.

더 많은 내용을 보고싶다면 중간에 참조사이트나 구글링을 하자.
제작자 : A반 김규동
"""
