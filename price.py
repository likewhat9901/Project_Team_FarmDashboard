import requests
import xmltodict
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

URL = "http://www.kamis.or.kr/service/price/xml.do?action=ItemInfo"

# 엑셀 읽기
df_items = pd.read_excel("./resData/items.xlsx")

def fetch_price_data(itemcategorycode, itemcode):
    today = datetime.today().strftime("%Y-%m-%d")
    params = {
        "p_cert_key": "85b4970a-81f2-417f-8bc2-b6815c6b3cf6",
        "p_productclscode": "01",
        "p_countycode": "1101",
        "p_regday": today,
        "p_itemcategorycode": str(itemcategorycode),
        "p_itemcode": str(itemcode),
        "p_convert_kg_yn": "Y",
        "p_cert_id": "5910",
        "p_returntype": "xml",
    }

    try:
        resp = requests.get(URL, params=params)
        resp.raise_for_status() # HTTP 응답 코드가 200(성공)이 아니면 오류(Exception)를 발생
        items = xmltodict.parse(resp.text)["document"]["data"].get("item") # xml을 Python 딕셔너리(dict)로 변환
        if not items:
            return []
        # countyname이 '평균', '최고값', '최저값', '등락률'이 아닌 것만 남기기
        filtered = [
            item for item in items
            if item.get("countyname") not in ["평균", "최고값", "최저값", "등락률"]
        ]
        return filtered

    except Exception as e:
        logging.error(f"[{itemcode}] 오류 발생: {e}")
        return []

def fetch_price_all(category_code="100"):
    all_data = []
    for _, row in df_items[df_items["부류코드"] == int(category_code)].iterrows():
        item_code = row["품목코드"]
        data = fetch_price_data(category_code, item_code)
        # 품목명을 붙이기
        for d in data:
            d["품목명"] = row["품목명"]
        all_data.extend(data)
    return all_data

def save_csv():
    category_codes = ["100", "200", "300", "400", "600"]  # 필요한 부류코드 다 넣기
    all_data = []

    for code in category_codes:
        data = fetch_price_all(code)
        for d in data:
            d["부류코드"] = code
        all_data.extend(data)

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv("./resData/가격_데이터.csv", index=False, encoding="utf-8-sig")
        print("CSV 저장 완료!")
    else:
        print("데이터 없음.")


save_csv()
# print(fetch_price_all())