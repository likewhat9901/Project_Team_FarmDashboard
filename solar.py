from flask import jsonify
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

def solar_data(region="서울"):
    
    # 6개 지역만
    stn_map = {
        '인천' : 102,
        '서울' : 108,
        '부산' : 253,
        '대구' : 137,
        '광주' : 156,
        '대전' : 133
    }
    
    load_dotenv()
    api_key = os.getenv('KMA_API_KEY')

    # 일사량조회 서비스
    url = 'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php'
    
    now = datetime.now()
    base_date = now.strftime('%Y%m%d')
    
    params = {
        'tm': base_date,
        'stn': stn_map[region],
        'help': 0,
        'authKey': api_key
    }
    
    # 텍스트 포맷에 맞는 컬럼 리스트
    columns = [
        "YYMMDDHHMI", "STN", "WD", "WS", "GST_WD", "GST_WS", "GST_TM",
        "PA", "PS", "PT", "PR", "TA", "TD", "HM", "PV", "RN_DAY",
        "RN_JUN", "RN_INT", "RN_HR3", "SD_DAY", "SD_TOT",
        "WC", "WP", "WW", "CA_TOT", "CA_MID", "CA_MIN", "CT_TOP", "CT_MID", "CT_LOW",
        "VS", "SS", "SI_5", "ST_10", "TS_20", "TE_30", "SEA", "WH", "BF", "IR", "IX"
    ]
    
    response = requests.get(url, params=params)
    # 텍스트 파싱
    lines = response.text.strip().split('\n')
    data_lines = [line for line in lines if not line.startswith('#') and line.strip()]

    if not data_lines:
        return jsonify({'error': '유효한 데이터 줄이 없음'}), 500

    values = data_lines[0].strip().split()
    result_dict = dict(zip(columns, values))

    solar_value = float(result_dict['ST_10']) * 277.78

    return {'solar_value': solar_value}
