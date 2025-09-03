from datetime import datetime, timedelta
from dotenv import load_dotenv
import os, xmltodict, requests, json

def weather_data(region="서울"):
    load_dotenv()
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        raise RuntimeError("WEATHER_API_KEY 가 .env에 없거나 로드되지 않음")

    # 지역 좌표 매핑
    region_coords = {
        "서울": {"nx": "60", "ny": "127"},
        "부산": {"nx": "98", "ny": "76"},
        "대구": {"nx": "89", "ny": "90"},
        "광주": {"nx": "58", "ny": "74"},
        "인천": {"nx": "55", "ny": "124"},
        "대전": {"nx": "67", "ny": "100"},
    }
    coords = region_coords.get(region, {"nx": "60", "ny": "127"})

    # 기준 시간 계산
    now = datetime.now()
    base_time = now.replace(minute=0, second=0, microsecond=0)
    if now.minute < 40:
        base_time -= timedelta(hours=1)

    base_date = base_time.strftime('%Y%m%d')
    base_time_str = base_time.strftime('%H%M')

    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
    params = {
        'serviceKey': api_key,
        'pageNo': '1',
        'numOfRows': '100',
        'dataType': 'XML',
        'base_date': base_date,
        'base_time': base_time_str,
        'nx': coords["nx"],
        'ny': coords["ny"]
    }

    response = requests.get(url, params=params)
    data_dict = xmltodict.parse(response.content)
    data_json = json.loads(json.dumps(data_dict, ensure_ascii=False))
    items = data_json['response']['body']['items']['item']

    category_map = {
        'T1H': '기온',
        'RN1': '1시간 강수량',
        'UUU': '동서바람성분',
        'VVV': '남북바람성분',
        'REH': '습도',
        'PTY': '강수형태',
        'VEC': '풍향',
        'WSD': '풍속'
    }

    weather_data = []
    for item in items:
        category = category_map.get(item["category"], item["category"])
        weather_data.append({
            "자료구분코드": category,
            "실황 값": item["obsrValue"]
        })

    temp_value = next(
        (i['실황 값'] for i in weather_data if i['자료구분코드'] == '기온'),
        None
    )
    humi_value = next(
        (i['실황 값'] for i in weather_data if i['자료구분코드'] == '습도'),
        None
    )
    rain_value = next(
        (i['실황 값'] for i in weather_data if i['자료구분코드'] == '1시간 강수량'),
        None
    )
    wind_value = next(
        (i['실황 값'] for i in weather_data if i['자료구분코드'] == '풍속'),
        None
    )

    return {
        'temp_value': temp_value,
        'humi_value': humi_value,
        'rain_value': rain_value,
        'wind_value': wind_value,
    }
