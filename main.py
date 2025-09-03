from flask import Flask, render_template, request, jsonify
from weather import weather_data
from solar import solar_data
from compare import compare_data
import pandas as pd
import os
from dotenv import load_dotenv
from outdoorplant import outdoor_json
from indoorplant import indoor_json
from pie import pie_data
from tensorflow.keras.models import load_model
import traceback
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np

app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>Welcome to Smart Farm Dashboard</h1>"

@app.route('/dashboard')
def dashboard():
    weather_dict = weather_data()
    compare_dict = compare_data()
    pie_plant1=pie_data("farm")
    pie_plant2=pie_data("foliage")

    return render_template(
        'dashboard.html',
        weather_dict=weather_dict,
        compare_dict=compare_dict,
        pie_plant1=pie_plant1,
        pie_plant2=pie_plant2
    )

@app.route('/education')
def education():
    return render_template('education.html')


@app.route('/flowershop')
def flowershop():
    return render_template('flowershop.html')

@app.route('/growplant')
def growplant():

    indoor_data = indoor_json()  
    outdoor_data = outdoor_json()
    plants = {
        "indoor": indoor_data,
        "outdoor": outdoor_data,
    }
    return render_template('growplant.html', plants=plants)

@app.route('/hurt')
def hurt():
    return render_template('hurt.html')

@app.route('/api/weather')
def api_weather():
    region = request.args.get("region", "서울")
    weather_dict = weather_data(region)
    return jsonify(weather_dict)



@app.route('/api/solar')
def api_solar():
    region = request.args.get("region", "서울")
    solar_dict = solar_data(region)
    return jsonify(solar_dict)


df = pd.read_csv("./resData/가격_데이터.csv")


@app.route('/api/get_ranking_data', methods=["POST"])
def get_ranking_data():
    req_data = request.get_json()
    category_code = int(req_data["category_code"])
    itemname = req_data.get("itemname")  # itemname이 안 올 수도 있으니 get()

    # 1차 필터링 (부류코드)
    filtered = df[df["부류코드"] == category_code]

    # 2차 필터링 (itemname이 있으면)
    if itemname:
        filtered = filtered[filtered["itemname"] == itemname]

    # NaN → None으로 변환
    filtered = filtered.where(pd.notna(filtered), None)
    data = filtered.to_dict(orient="records")

    return jsonify(data)



@app.errorhandler(404) 
def page_not_found(error):
    print('오류 로그:', error) # 서버 콘솔에 출력
    return "페이지가 없습니다. URL를 확인하세요.", 404

# 한이 식물성장예측
# load_dotenv()
# api_key = os.getenv('WEATHER_API_KEY')

# @app.route("/predict")
# def plant_predict():
#     plants = get_prediction()
#     return render_template(
#         'predict.html',
#         plants=plants
#     )

# def get_prediction():
#     predict_indoordict = indoor_json()
#     predict_outdoordict = outdoor_json()
#     result = {
#         "indoor" : predict_indoordict,
#         "outdoor" : predict_outdoordict
#     }
#     return result
MODEL_INFO = {
    '딸기': {
        'path': 'C:/02Workspace/Project3/Project-cheon/saveFiles/strawberry_cnn_model.h5',
        'categories': ["잿빛곰팡이병", "정상", "흰가루병"],
        'input_size': (64, 64)
    },
    # 귤, 레몬, 참외 등 필요시 추가
}

models = {fruit: load_model(info['path']) for fruit, info in MODEL_INFO.items()}

def preprocess_image(image_file, target_size):
    img = Image.open(image_file).convert('RGB')
    img = img.resize(target_size)
    img_array = img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

@app.route('/plant_disease')
def plant_disease():
    fruits = list(MODEL_INFO.keys())
    return render_template('plant_disease.html', fruits=fruits)

@app.route('/predict', methods=['POST'])
def predict():
    fruit = request.form.get('fruit')
    image = request.files.get('image')

    if not fruit or fruit not in models:
        return jsonify({'error': '지원하지 않는 과일입니다.'}), 400
    if not image:
        return jsonify({'error': '이미지를 첨부해주세요.'}), 400

    try:
        info = MODEL_INFO[fruit]
        input_data = preprocess_image(image, info['input_size'])
        prediction = models[fruit].predict(input_data)
        idx = int(np.argmax(prediction))
        confidence = float(prediction[0][idx])
        disease = info['categories'][idx]

        return jsonify({'disease': disease, 'confidence': confidence})
    except Exception as e:
        traceback.print_exc()  # 여기가 바로 에러 로그 찍는 부분
        return jsonify({'error': '서버 에러 발생: ' + str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    





