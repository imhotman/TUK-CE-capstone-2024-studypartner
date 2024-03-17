from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from study.settings import BASE_DIR   # Django settings.py 파일에서 BASE_DIR을 가져옴
from sklearn.preprocessing import PolynomialFeatures    # 다항 특성을 만들기 위한 모듈
from sklearn.linear_model import LinearRegression   # 선형 회귀 모델
from pathlib import Path    # 파일 경로를 다루기 위한 모듈
from datetime import date   # 현재 날짜를 얻기 위한 모듈
from .forms import ForecastForm   # 예측 폼을 가져옴
import pandas as pd # 데이터프레임을 다루기 위한 모듈

# data.csv 파일을 읽어들여 DataFrame 객체로 저장
DF_MAIN = pd.read_csv(BASE_DIR / 'data.csv', encoding='cp949')

# 각 에너지 사용량에 대한 예측을 계산하는 함수
def calculate_prediction(X, y, year):
    poly_features = PolynomialFeatures(degree=3, include_bias=False)
    X_poly = poly_features.fit_transform(X.reshape(-1, 1))
    lin_reg = LinearRegression()
    lin_reg.fit(X_poly, y)
    r2 = lin_reg.score(X_poly, y)
    r2_percent = r2 * 100
    predictions = lin_reg.predict(poly_features.transform([[year]]))
    
    # 예측값이 음수일 경우 표시하는 에러 메시지
    if predictions[0] < 0:
        predicted_message = "유효한 예측값이 아닙니다." 
        r2_percent = "측정불가"

    # 예측값이 양수일 경우 표시하는 메시지
    else:
        predicted_message = f'{predictions[0]:,.2f}'
        r2_percent = f'{r2_percent:.2f}'

    return predicted_message, r2_percent


# 웹 애플리케이션의 루트 URL에 접속했을 때 'index.html' 템플릿을 보여주는 역할
def index(request: HttpRequest) -> HttpResponse:
    data = {}

    if request.method == 'POST':
        # POST 요청에서 폼 데이터 추출
        form = ForecastForm(request.POST)

        if form.is_valid():
            year = form.cleaned_data['year']
            month = int(form.cleaned_data['month'])
            district = form.cleaned_data['district']
            town = form.cleaned_data['town']

            # 전기 사용량 데이터 처리
            df_elec = DF_MAIN[(DF_MAIN['월'] == month) & (DF_MAIN['구'] == district) & (DF_MAIN['동'] == town)][['년도', '전기']]
            X_elec = df_elec['년도'].values
            y_elec = df_elec['전기'].values
            data['electric'], r2_percent_elec = calculate_prediction(X_elec, y_elec, year)

            # 수도 사용량 데이터 처리
            df_water = DF_MAIN[(DF_MAIN['월'] == month) & (DF_MAIN['구'] == district) & (DF_MAIN['동'] == town)][['년도', '수도']]
            X_water = df_water['년도'].values
            y_water = df_water['수도'].values
            data['water'], r2_percent_water = calculate_prediction(X_water, y_water, year)

            # 도시가스 사용량 데이터 처리
            df_gas = DF_MAIN[(DF_MAIN['월'] == month) & (DF_MAIN['구'] == district) & (DF_MAIN['동'] == town)][['년도', '가스']]
            X_gas = df_gas['년도'].values
            y_gas = df_gas['가스'].values
            data['gas'], r2_percent_gas = calculate_prediction(X_gas, y_gas, year)

            # 탄소 사용량 데이터 처리
            df_carbon = DF_MAIN[(DF_MAIN['월'] == month) & (DF_MAIN['구'] == district) & (DF_MAIN['동'] == town)][['년도', '탄소']]
            X_carbon = df_carbon['년도'].values
            y_carbon = df_carbon['탄소'].values
            data['carbon'], r2_percent_carbon = calculate_prediction(X_carbon, y_carbon, year)

            data['comment'] = f'{year}년 {month}월 서울시 {district} {town} 에너지 사용 예측량입니다.'

            form = ForecastForm()
    elif request.method == 'GET':
        # GET 요청인 경우 처리
        form = ForecastForm()

    context = {
        'date': date.today().isoformat(),
        'form': form,
        'comment': "현재 날짜보다 예측 년도/월이 높아야 합니다." if form.errors else data.get('comment', '예측 하기 버튼을 눌러주세요.'),
        'electric': data.get('electric', '-'),
        'water': data.get('water', '-'),
        'gas': data.get('gas', '-'),
        'carbon': data.get('carbon', '-'),
    }

    return render(request, 'study/index.html', context)

def signup(request: HttpRequest) -> HttpResponse: # 회원가입 페이지
    return render(request, 'study/signup.html')

def signup_done(request: HttpRequest) -> HttpResponse: # 회원가입 완료 페이지
    return render(request, 'study/signup_done.html')

def login(request: HttpRequest) -> HttpResponse: # 로그인 페이지
    return render(request, 'study/login.html')

def logout(request: HttpRequest) -> HttpResponse: # 로그아웃 페이지
    return render(request, 'study/logout.html')

def about(request: HttpRequest) -> HttpResponse: # 소개 페이지
    return render(request, 'study/about.html')

def mypage(request: HttpRequest) -> HttpResponse: # 마이페이지
    return render(request, 'study/mypage.html')

def notice(request: HttpRequest) -> HttpResponse: # 공지사항
    return render(request, 'study/notice.html')

def qna(request: HttpRequest) -> HttpResponse: # Q&A
    return render(request, 'study/qna.html')

def lecture(request: HttpRequest) -> HttpResponse: # 강의실
    return render(request, 'study/lecture.html')

def chapter(request: HttpRequest) -> HttpResponse: # 강의실_각 챕터
    return render(request, 'study/chapter.html')


