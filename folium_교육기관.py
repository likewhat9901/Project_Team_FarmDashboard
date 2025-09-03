# 모듈 임포트
import pandas as pd
import folium

# CSV 경로
csv_path = './resData/도시농업_교육기관_좌표_결과.csv'

# CSV 읽기
df = pd.read_csv(csv_path)

# folium으로 지도 생성
edu_map = folium.Map(location=[37.47, 126.88], zoom_start=9)

# 마커 생성
for _, row in df.iterrows():
    print(f"DEBUG: {row['표시이름']} - 주소: {row['주소']} / 위도: {row['위도']} / 경도: {row['경도']}")
    faclt = row['표시이름']
    addr = row['주소']
    latitude = row['위도']
    longitude = row['경도']

    if pd.notnull(latitude) and pd.notnull(longitude):
        try:
            lat = float(latitude)
            lon = float(longitude)
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(f"<b>{faclt}</b><br>{addr}", max_width=300),
                icon=folium.Icon(color='blue', icon='star')
            ).add_to(edu_map)
            print(f"[마커 추가] {faclt} - {lat}, {lon}")
        except ValueError:
            print(f"[오류] 좌표 변환 실패 - {faclt}")

# 지도 저장
edu_map.save('./saveFiles/edu_map_marker.html')
print("맵이 생성되었습니다: edu_map_marker.html")