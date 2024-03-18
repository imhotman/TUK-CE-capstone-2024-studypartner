from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from study.settings import BASE_DIR   # Django settings.py 파일에서 BASE_DIR을 가져옴
from pathlib import Path    # 파일 경로를 다루기 위한 모듈
from datetime import date   # 현재 날짜를 얻기 위한 모듈







def index(request: HttpRequest) -> HttpResponse: # 메인 페이지
    return render(request, 'study/index.html')



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

# def lecture(request: HttpRequest) -> HttpResponse: # 강의실
#     return render(request, 'study/lecture.html')

def chapter(request: HttpRequest) -> HttpResponse: # 강의실_각 챕터
    return render(request, 'study/chapter.html')


