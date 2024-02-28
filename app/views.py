from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from eco.settings import BASE_DIR   # Django settings.py 파일에서 BASE_DIR을 가져옴
from sklearn.preprocessing import PolynomialFeatures    # 다항 특성을 만들기 위한 모듈
from sklearn.linear_model import LinearRegression   # 선형 회귀 모델
from pathlib import Path    # 파일 경로를 다루기 위한 모듈
from datetime import date   # 현재 날짜를 얻기 위한 모듈
import pandas as pd # 데이터프레임을 다루기 위한 모듈

# data.csv 파일을 읽어들여 DataFrame 객체로 저장
DF_MAIN = pd.read_csv(BASE_DIR / 'data.csv', encoding='cp949')



# --- 이곳에 웹 애플리케이션의 뷰 로직 추가 ---

# 웹 애플리케이션의 루트 URL에 접속했을 때 'index.html' 템플릿을 보여주는 역할
def index(request: HttpRequest) -> HttpResponse:    # index.html 템플릿을 렌더링하여 HttpResponse로 반환
    return render(request, 'index.html')


# 전기 사용량을 예측하는 Django 뷰(View) 함수
def predict_elec(request: HttpRequest, month: int, district: str, town: str) -> HttpResponse:
    df = DF_MAIN[(DF_MAIN['월'] == month) & (DF_MAIN['구'] == district) & (DF_MAIN['동'] == town)][['년도', '전기']]    # 주어진 월, 구, 동에 해당하는 데이터를 필터링하여 DataFrame으로 저장

    X = df['년도'].values
    y = df['전기'].values

    poly_features = PolynomialFeatures(degree=5, include_bias=False)
    X_poly = poly_features.fit_transform(X.reshape(-1, 1))

    lin_reg = LinearRegression()
    lin_reg.fit(X_poly, y)

    return HttpResponse(f'Predicted electricity usage for {town} in {district} in {month} is {lin_reg.predict(poly_features.transform([[date.today().year]]))}')



