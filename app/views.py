from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from study.settings import BASE_DIR   # Django settings.py 파일에서 BASE_DIR을 가져옴
from pathlib import Path    # 파일 경로를 다루기 위한 모듈
from user.models import Study_TimerSession
from datetime import datetime, timedelta, timezone
import pytz




def index(request: HttpRequest) -> HttpResponse: # 메인 페이지
    return render(request, 'study/index.html')

def signup(request: HttpRequest) -> HttpResponse: # 회원가입 페이지
    return render(request, 'study/signup.html')

def signup_done(request: HttpRequest) -> HttpResponse: # 회원가입 완료 페이지
    return render(request, 'study/signup_done.html')

def delete_done(request: HttpRequest) -> HttpResponse: # 회원탈퇴 완료 페이지
    return render(request, 'study/delete_done.html')

def login(request: HttpRequest) -> HttpResponse: # 로그인 페이지
    return render(request, 'study/login.html')

def logout(request: HttpRequest) -> HttpResponse: # 로그아웃 페이지
    return render(request, 'study/logout.html')

def about(request: HttpRequest) -> HttpResponse: # 소개 페이지
    return render(request, 'study/about.html')

# def mypage(request: HttpRequest) -> HttpResponse: # 마이페이지
#     return render(request, 'study/mypage.html')

# 마이페이지
# def mypage(request):
#     if request.user.is_authenticated:
#         # 현재 사용자의 Study_TimerSession 모델에서 모든 객체 가져오기
#         # sessions = Study_TimerSession.objects.filter(user=request.user) # 오름차순 정렬
#         sessions = Study_TimerSession.objects.filter(user=request.user).order_by('-date')   # 내림차순 정렬

            
#         # 기록을 timedelta 형식으로 변환
#         for session in sessions:
#             session.records = convert_to_timedelta(session.records)

#         # 가장 높은 기록을 가진 객체 찾기
#         if sessions:
#             highest_record = max(sessions, key=lambda session: convert_to_day(session.records))
#         else:
#             highest_record = None

#         context = {
#             'sessions': sessions,
#             'highest_record': highest_record
#         }
#     else:
#         # 세션에 로그인되어 있지 않은 경우
#         context = {'message': '로그인 되지 않았습니다.'}
    
#     return render(request, 'study/mypage.html', context)
def mypage(request: HttpRequest) -> HttpResponse: # 마이페이지
    if request.user.is_authenticated:
        # 현재 사용자의 Study_TimerSession 모델에서 모든 객체 가져오기
        sessions = Study_TimerSession.objects.filter(user=request.user).order_by('-date') # 내림차순 정렬

        # 기록을 timedelta 형식으로 변환
        for session in sessions:
            session.records = convert_to_timedelta(session.records)

        # 한국 시간대로 변환
        korea_tz = pytz.timezone('Asia/Seoul')
        for session in sessions:
            session.date = session.date.astimezone(korea_tz)

        # 각 날짜별로 가장 높은 기록을 가진 객체 찾기
        highest_records = []
        if sessions:
            previous_date = sessions[0].date.date()
            highest_record = sessions[0]
            for session in sessions[1:]:
                current_date = session.date.date()
                if current_date != previous_date:
                    highest_records.append(highest_record)
                    highest_record = session
                    previous_date = current_date
                else:
                    if convert_to_day(session.records) > convert_to_day(highest_record.records):
                        highest_record = session
            highest_records.append(highest_record)

        else:
            highest_records = None

        context = {
            'sessions': sessions,
            'highest_records': highest_records
        }

    else:
        # 세션에 로그인되어 있지 않은 경우
        context = {'message': '로그인 되지 않았습니다.'}
    
    return render(request, 'study/mypage.html', context)




def notice(request: HttpRequest) -> HttpResponse: # 공지사항
    return render(request, 'study/notice.html')

def qna(request: HttpRequest) -> HttpResponse: # Q&A
    return render(request, 'study/qna.html')

# def lecture(request: HttpRequest) -> HttpResponse: # 강의실
#     return render(request, 'study/lecture.html')

def chapter(request: HttpRequest) -> HttpResponse: # 강의실_각 챕터
    return render(request, 'study/chapter.html')


# 시간 문자열을 시간으로 변환
def convert_to_timedelta(record):
    # 시간 문자열을 ':'로 분할하여 시, 분, 초를 추출
    hours, minutes, seconds = map(int, record.split(':'))
    # timedelta 객체로 변환하여 반환
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


# 하루 단위 기록
def convert_to_day(record):
    # 기록을 초로 변환
    total_seconds = record.total_seconds()
    # 하루(24시간)에 해당하는 초로 나누어 하루 단위의 기록을 구함
    return total_seconds / 86400


# 타이머 기록 삭제 - 마이페이지 전용
def delete_record_view(request, record_id):
    if request.method == 'POST':
        # POST 요청인 경우에만 실행
        try:
            # 기록 객체 가져오기
            record = Study_TimerSession.objects.get(pk=record_id)
            # 기록 삭제
            record.delete()
        except Study_TimerSession.DoesNotExist:
            # 해당 기록이 존재하지 않는 경우 처리
            pass
    # 기록 삭제 후에는 마이페이지로 리다이렉트
    return redirect('mypage')


# 타이머 기록 삭제 - 공부기록 관리 페이지 전용
def delete_studyrecord_view(request, record_id):
    if request.method == 'POST':
        # POST 요청인 경우에만 실행
        try:
            # 기록 객체 가져오기
            record = Study_TimerSession.objects.get(pk=record_id)
            # 기록 삭제
            record.delete()
        except Study_TimerSession.DoesNotExist:
            # 해당 기록이 존재하지 않는 경우 처리
            pass
    # 기록 삭제 후에는 마이페이지로 리다이렉트
    return redirect('user:study_recordpage')