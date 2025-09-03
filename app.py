from flask import Flask, jsonify, render_template
import os
from dotenv import load_dotenv
from outdoorplant import outdoor_json
from indoorplant import indoor_json

load_dotenv()
api_key = os.getenv('WEATHER_API_KEY')
app = Flask(__name__)

@app.route("/predict")
def plant_predict():
    plants = get_prediction()
    return render_template(
        'predict.html',
        plants=plants
    )

def get_prediction():
    predict_indoordict = indoor_json()
    predict_outdoordict = outdoor_json()
    result = {
        "indoor" : predict_indoordict,
        "outdoor" : predict_outdoordict
    }
    return result

if __name__ == '__main__':
    app.run(debug=True)
