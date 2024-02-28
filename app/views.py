from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from eco.settings import BASE_DIR
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from pathlib import Path
from datetime import date
import pandas as pd


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello, Django!')

def predict_elec(request: HttpRequest, month: int, district: str, town: str) -> HttpResponse:
    df = pd.read_csv(BASE_DIR / 'data.csv', encoding='cp949')
    df[(df['월'] == month) & (df['구'] == district) & (df['동'] == town)][['년도', '전기']]

    X = df['년도'].values
    y = df['전기'].values

    poly_features = PolynomialFeatures(degree=5, include_bias=False)
    X_poly = poly_features.fit_transform(X.reshape(-1, 1))

    lin_reg = LinearRegression()
    lin_reg.fit(X_poly, y)

    return HttpResponse(f'Predicted electricity usage for {town} in {district} in {month} is {lin_reg.predict(poly_features.transform([[date.today().year]]))}')



