import pandas as pd
from sklearn.svm import SVR
import numpy as np
import json

# 데이터 로드(텃밭식물만)
# 실내식물 : 몬스테라, 스투키, 오렌지쟈스민, 홍콩야자
# 텃밭식물 : 방울토마토, 오이, 파프리카

indoor_plants_files = [
    "./resData/방울토마토.csv",
    "./resData/오이.csv",
    "./resData/파프리카.csv"
]

def outdoor_json():
    results = {}
    for file_path in indoor_plants_files:
        # 식물 이름 추출 (예: 몬스테라.csv -> 몬스테라)
        plant_name = file_path.split('/')[-1].replace('.csv', '')

        df = pd.read_csv(file_path)
        X = df[['date']].values
        y_height = df['height'].values
        y_fruitnum = df['fruitnum'].values

        # SVR 모델 학습 - 길이
        svr_height = SVR(kernel='rbf', C=100, epsilon=0.1)
        svr_height.fit(X, y_height)

        # SVR 모델 학습 - 열매 개수
        svr_fruit = SVR(kernel='rbf', C=100, epsilon=0.1)
        svr_fruit.fit(X, y_fruitnum)

        # 예측용 데이터 생성
        X_plot = np.linspace(X.min(), X.max() + 2, 200).reshape(-1, 1)
        y_height_plot = svr_height.predict(X_plot)
        y_fruit_plot = svr_fruit.predict(X_plot)

        # 다음 주차 예측
        next_week = X.max() + 1
        pred_height = svr_height.predict([[next_week]])[0]
        pred_fruit = svr_fruit.predict([[next_week]])[0]

        print("길이 예측값:", pred_height, "열매수 예측값:", pred_fruit)
        # 원본 데이터를 JSON 직렬화 가능한 형태로 변환
        data_with_prediction = []
        for _, row in df.iterrows():
            data_with_prediction.append({
                'date': int(row['date']),  # numpy int를 파이썬 int로 변환
                'height': float(row['height']),  # numpy float를 파이썬 float로 변환
                'fruitnum': float(row['fruitnum'])  # numpy float를 파이썬 float로 변환
            })

        # 예측값 추가 (이미 파이썬 기본 타입으로 변환됨)
        data_with_prediction.append({
            'date': int(next_week),
            'height': float(round(pred_height, 2)),
            'fruitnum': float(round(pred_fruit, 2))
        })

        results[plant_name] = data_with_prediction

    return results

# JSON 직렬화 확인
result = outdoor_json()
print(json.dumps(result, indent=2, ensure_ascii=False))