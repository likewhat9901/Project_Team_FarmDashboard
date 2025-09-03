import pandas as pd
from sklearn.svm import SVR

# 데이터 로드(실내식물만)
# 실내식물 : 몬스테라, 스투키, 오렌지쟈스민, 홍콩야자
# 텃밭식물 : 방울토마토, 오이, 파프리카

indoor_plants_files = [
    "./resData/몬스테라.csv",
    "./resData/스투키.csv",
    "./resData/오렌지쟈스민.csv",
    "./resData/홍콩야자.csv"
]

def indoor_json():
    results = {}
    for file_path in indoor_plants_files:
        # 식물 이름 추출 (예: 몬스테라.csv -> 몬스테라)
        plant_name = file_path.split('/')[-1].replace('.csv', '')

        df = pd.read_csv(file_path)
        X = df[['date']].values
        y = df['height'].values

        # SVR 모델 학습
        svr_model = SVR(kernel='rbf', C=100, gamma='scale', epsilon=0.1)
        svr_model.fit(X, y)

        # 다음 주차 예측
        next_week = df['date'].max() + 1
        next_week_pred = svr_model.predict([[next_week]])[0]

        # 원본 데이터 + 예측값 포함 리스트 생성
        data_with_prediction = []
        for record in df.to_dict(orient='records'):
            data_with_prediction.append({
                'date': int(record['date']),
                'height': float(record['height'])
            })
        data_with_prediction.append({
            'date': int(next_week),
            'height': float(round(next_week_pred, 2))
        })
        results[plant_name] = data_with_prediction

    return results

print(indoor_json())