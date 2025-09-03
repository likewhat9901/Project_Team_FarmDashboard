import pandas as pd
import folium, glob
from folium import FeatureGroup
from folium.plugins import MarkerCluster

# 여러 CSV 읽기
file_list = glob.glob('./resData/전국_꽃집_주소/*.csv')

df_list = []
for file in file_list:
    try:
        df_part = pd.read_csv(file, encoding='utf-8')
    except UnicodeDecodeError:
        df_part = pd.read_csv(file, encoding='cp949')
    df_list.append(df_part)

df = pd.concat(df_list, ignore_index=True)


# 시군명 목록
sigun_list = sorted(
    s for s in df['시도명'].dropna().unique()
    if not str(s).strip().isdigit()
)

# 지도 초기화
flowershop_map = folium.Map(location=[37.40, 127.38], zoom_start=9, tiles=None)
# 사용자 정의 이름으로 타일 추가
folium.TileLayer('OpenStreetMap', name='지역선택').add_to(flowershop_map)


# 시군별 그룹 + 클러스터 마커 생성
for sigun in sigun_list:
    group = FeatureGroup(
        name=sigun,
        show=(sigun in ["서울특별시", "경기도"])
    )
    marker_cluster = MarkerCluster().add_to(group)

    # 해당 시군 데이터만 필터
    sigun_data = df[df['시도명'] == sigun]

    for _, row in sigun_data.iterrows():
        print(f"DEBUG: {row['상호명']} - 위도: {row['위도']} / 경도: {row['경도']}")
        faclt = row['상호명']
        lat = row['위도']
        lon = row['경도']

        if pd.notnull(lat) and pd.notnull(lon):
            try:
                lat = float(lat)
                lon = float(lon)
                folium.Marker(
                    [lat, lon],
                    popup=folium.Popup(f"<b>{faclt}</b>", max_width=250),
                    icon=folium.Icon(color="green", icon="leaf")
                ).add_to(marker_cluster)
            except ValueError:
                print(f"[오류] 좌표 변환 실패 - {faclt}")

    group.add_to(flowershop_map)

# 레이어 컨트롤
folium.LayerControl(collapsed=False).add_to(flowershop_map)

# 지도 저장
flowershop_map.save('./saveFiles/flowershop_map.html')
print("맵이 생성되었습니다: flowershop_map.html")
