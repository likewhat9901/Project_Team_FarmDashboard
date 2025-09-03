from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import os

# 1. 모델 불러오기
model_path = "D:/project-js/project-js/strawberry_cnn_model.h5"
model = load_model(model_path)

# 2. 클래스 이름 정의 (카테고리 리스트와 순서 같아야 함)
categories = ["잿빛곰팡이병", "정상", "흰가루병"]

# 3. 예측용 이미지 불러오기 및 전처리 함수
def preprocess_image(image_path, target_size=(64, 64)):  # 모델 input shape와 맞춤
    img = Image.open(image_path)
    img = img.convert('RGB')
    img = img.resize(target_size)
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # 배치 차원 추가
    return img_array

# 테스트용/나중에 필요할때 하장
# 4. 이미지 경로 지정
# image_path1 = 'C:/02WorkSpaces/Aihub/strawberry/testfiles/strawberry_gray_mold/10.jpg'


# # 5. 이미지 전처리
# input_data1 = preprocess_image(image_path1)


# # 6. 예측
# pred1 = model.predict(input_data1)


# predicted_index1 = np.argmax(pred1)
# confidence1 = pred1[0][predicted_index1]


# # 7. 결과 출력
# print(f"예측 결과: {categories[predicted_index1]}")
# print(f"신뢰도: {confidence1 * 100:.2f}%")
