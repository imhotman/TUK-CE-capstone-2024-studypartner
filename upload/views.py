from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, redirect
from django.contrib.auth.models import User
from user.models import Lecture, LectureChapter
from django.urls import reverse
from django.http import HttpResponse



def chapter_detail_view(request, lecture_name, chapter_name):
    # 강의명과 챕터명이 일치하는 LectureChapter 객체를 가져옴
    chapter = LectureChapter.objects.filter(lecture__title=lecture_name, chapter_name=chapter_name).first()

    # 현재 로그인한 사용자 정보를 가져옴
    current_user = request.user
    lecture_chapters = LectureChapter.objects.filter(user=current_user).select_related('lecture').order_by('lecture__title')

    # LectureChapter가 없는 경우 404 에러 반환
    if not chapter:
        raise Http404("챕터를 찾을 수 없습니다.")

    lectures = []
    for chapter_obj in lecture_chapters:
        lecture_title = chapter_obj.lecture.title
        chapter_name = chapter_obj.chapter_name
        lecture_url = reverse('user:lecture_detail', kwargs={'lecture_name': lecture_title})
        chapter_url = reverse('upload:chapter_detail', kwargs={'lecture_name': lecture_title, 'chapter_name': chapter_name})

        # 현재 강의가 lectures 리스트에 없으면 추가
        if not any(lecture['lecture'] == lecture_title for lecture in lectures):
            lectures.append({'lecture': lecture_title, 'chapters': []})

        # 현재 챕터 추가
        lectures[-1]['chapters'].append({'chapter_name': chapter_name, 'chapter_url': chapter_url, 'lecture_url': lecture_url})


    context = {
        'chapter': chapter,
        'lectures': lectures,
        'chapter_name': chapter_name
    }

    return render(request, "upload/chapter_detail.html", context)













def test1_view(request):
    return render(request, "upload/test1.html")

def test2_view(request):
    return render(request, "upload/test2.html")










from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime

# 타이머 변수
timer_running = False
start_time = None
elapsed_time = 0
records = []

# 타이머 시작
def start_timer(request):
    global timer_running, start_time, elapsed_time
    if not timer_running:
        timer_running = True
        start_time = datetime.now()
    return JsonResponse({'message': 'Timer started.'})

# 타이머 중지
def stop_timer(request):
    global timer_running, start_time, elapsed_time
    if timer_running:
        timer_running = False
        elapsed_time += (datetime.now() - start_time).total_seconds()
    return JsonResponse({'message': 'Timer stopped.'})

# 기록 저장
def record_time(request):
    global records, elapsed_time
    if elapsed_time > 0:
        records.append(elapsed_time)
        elapsed_time = 0
    return JsonResponse({'message': 'Time recorded.'})


# HTML 페이지 렌더링
def timer_view(request):
    global timer_running, start_time, elapsed_time, records
    context = {'timer_running': timer_running, 'elapsed_time': elapsed_time, 'records': records}
    return render(request, 'upload/timer.html', context)

