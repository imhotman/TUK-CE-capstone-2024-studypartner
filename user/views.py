from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Lecture, LectureChapter, Study_TimerSession
from django.contrib.auth.decorators import login_required
from .forms import LectureChapterForm
from django.urls import reverse
from django.http import JsonResponse
from .models import Study_TimerSession
from datetime import datetime, timedelta, timezone
import json


# 로그인
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(username=username, password=password)

        if user is not None:
            print("로그인 성공")
            messages.success(request, "로그인 성공!")
            login(request, user)
            return redirect("index")  # 로그인 성공 시 index 페이지로 리다이렉트
        else:
            messages.error(request, "로그인 실패")
            print("로그인 실패")

    return render(request, "user/login.html")


# 로그아웃
def logout_view(request):
    logout(request)
    request.session.clear()  # 세션 내용을 삭제
    print("로그아웃")
    return redirect("index")


# 회원가입
def signup_view(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "회원가입 성공!")
        print("회원가입 성공")
        return redirect("signup_done")

    return render(request, "user/signup.html")


# 회원탈퇴
def delete_account_view(request):
    if request.method == "POST":
        # 현재 로그인한 사용자를 가져옴.
        user = request.user
        print(f"삭제할 사용자: {user}")
        # 회원정보 삭제
        user.delete()
        print("회원 탈퇴완료")

        # 로그아웃
        logout(request)

        # 삭제 후 리다이렉트할 페이지를 지정
        return redirect("delete_done")

    # POST 요청이 아니면 일반적으로 회원탈퇴를 수행하는 폼 제공
    print("GET 요청입니다.")
    return redirect("index")








# 수정할 페이지
# 삭제예정 - lecture_list_view
@login_required
def lecture_list_view(request):
    user = request.user
    lecture_chapters = LectureChapter.objects.filter(user=user).select_related('lecture').order_by('lecture__title')

    lectures = []
    for chapter in lecture_chapters:
        lecture_title = chapter.lecture.title
        chapter_name = chapter.chapter_name
        lecture_url = reverse('user:lecture_detail', kwargs={'lecture_name': lecture_title})
        chapter_url = reverse('upload:chapter_detail', kwargs={'lecture_name': lecture_title, 'chapter_name': chapter_name})

        # 현재 강의가 lectures 리스트에 없으면 추가
        if not any(lecture['lecture'] == lecture_title for lecture in lectures):
            lectures.append({'lecture': lecture_title, 'chapters': []})

        # 현재 챕터 추가
        lectures[-1]['chapters'].append({'chapter_name': chapter_name, 'chapter_url': chapter_url, 'lecture_url': lecture_url})

    context = {
        'lectures': lectures,
    }
    return render(request, "user/lecture_list.html", context)








# 강의실
@login_required
def lecture_view(request):
    user = request.user
    lecture_chapters = LectureChapter.objects.filter(user=user).select_related('lecture').order_by('lecture__title')

    lectures = []
    for chapter in lecture_chapters:
        lecture_title = chapter.lecture.title
        chapter_name = chapter.chapter_name
        lecture_url = reverse('user:lecture_detail', kwargs={'lecture_name': lecture_title})
        chapter_url = reverse('upload:chapter_detail', kwargs={'lecture_name': lecture_title, 'chapter_name': chapter_name})

        # 현재 강의가 lectures 리스트에 없으면 추가
        if not any(lecture['lecture'] == lecture_title for lecture in lectures):
            lectures.append({'lecture': lecture_title, 'chapters': []})

        # 현재 챕터 추가
        lectures[-1]['chapters'].append({'chapter_name': chapter_name, 'chapter_url': chapter_url, 'lecture_url': lecture_url})

    context = {
        'lectures': lectures,
    }
    return render(request, "user/lecture.html", context)


# 강의 추가
@login_required
def add_lecture_chapter_view(request):
    if request.method == 'POST':
        form = LectureChapterForm(request.POST)
        if form.is_valid():
            # 폼에서 입력한 데이터 가져오기
            lecture_name = form.cleaned_data.get('lecture_name')
            chapter_name = form.cleaned_data.get('chapter_name')

            # 현재 사용자의 lecture_name이 이미 존재하는지 확인
            existing_lecture = LectureChapter.objects.filter(user=request.user, lecture__title=lecture_name).first()

            if existing_lecture:
                # 해당 lecture_name이 이미 존재하는 경우
                # lecture_name에 하위 목록 추가
                LectureChapter.objects.create(user=request.user, lecture=existing_lecture.lecture, chapter_name=chapter_name)
                print("기존 강의에 챕터를 추가하였습니다.")
            else:
                # 해당 lecture_name이 존재하지 않는 경우
                # 새로운 강의 및 챕터 추가
                lecture = Lecture.objects.create(title=lecture_name)
                LectureChapter.objects.create(user=request.user, lecture=lecture, chapter_name=chapter_name)
                print("새로운 강의 및 챕터를 추가하였습니다.")

            messages.success(request, '강의 챕터가 성공적으로 추가되었습니다.')
            return render(request, "user/add_lecture_chapter.html")
    else:
        form = LectureChapterForm()

    # 폼 유효성 검사 실패 시에도 폼과 함께 에러 메시지를 전달
    if form.errors:
        # 폼에서 입력한 데이터 가져오기
        lecture_name = form.cleaned_data.get('lecture_name')
        chapter_name = form.cleaned_data.get('chapter_name')
        
        # 터미널에 출력
        print("User:", request.user)
        print("Lecture:", lecture_name)
        print("Chapter Name:", chapter_name)
        print("강의 챕터 추가에 실패했습니다.")

        messages.error(request, '강의 챕터 추가에 실패했습니다. 입력을 다시 확인해주세요.')
        print("강의 챕터 추가에 실패했습니다.")

    return render(request, 'user/add_lecture_chapter.html')






# def lecture_detail_view(request, lecture_name):
#     # 강의명이 주어진 문자열을 포함하는 모든 LectureChapter 객체를 가져옴
#     lecture_chapters = LectureChapter.objects.filter(lecture__title__contains=lecture_name)

#     # LectureChapter가 없는 경우 404 에러 반환
#     if not lecture_chapters.exists():
#         raise Http404("강의를 찾을 수 없습니다.")

#     # 만약 LectureChapter가 여러 개인 경우 첫 번째 LectureChapter를 선택
#     lecture_chapter = lecture_chapters.first()

#     # 강의에 대한 추가적인 정보를 가져오거나 생성하는 코드 작성

#     context = {
#         'lecture_chapter': lecture_chapter,
#         # 강의에 관련된 다른 정보를 추가할 수 있음
#     }

#     return render(request, "user/lecture_detail.html", context)


# 강의 상세정보
def lecture_detail_view(request, lecture_name):
    # 강의명에 해당하는 모든 LectureChapter 객체를 가져옴
    lecture_chapters = LectureChapter.objects.filter(lecture__title=lecture_name)

    # LectureChapter가 없는 경우 404 에러 반환
    if not lecture_chapters.exists():
        raise Http404("해당 강의에 대한 챕터를 찾을 수 없습니다.")

    # 현재 유저의 강의 목록과 챕터 목록 가져오기
    user = request.user
    lecture_chapters_user = LectureChapter.objects.filter(user=user).select_related('lecture').order_by('lecture__title')

    lectures = []
    for chapter in lecture_chapters_user:
        lecture_title = chapter.lecture.title
        chapter_name = chapter.chapter_name
        lecture_url = reverse('user:lecture_detail', kwargs={'lecture_name': lecture_title})
        chapter_url = reverse('upload:chapter_detail', kwargs={'lecture_name': lecture_title, 'chapter_name': chapter_name})

        # 현재 강의가 lectures 리스트에 없으면 추가
        if not any(lecture['lecture'] == lecture_title for lecture in lectures):
            lectures.append({'lecture': lecture_title, 'chapters': []})

        # 현재 챕터 추가
        lectures[-1]['chapters'].append({'chapter_name': chapter_name, 'chapter_url': chapter_url, 'lecture_url': lecture_url})

    context = {
        'lecture_name': lecture_name,
        'lecture_chapters': lecture_chapters,
        'lectures': lectures,
    }

    return render(request, "user/lecture_detail.html", context)






# 세션 키 정의
TIMER_SESSION_KEYS = {
    'TIMER_RUNNING': 'timer_running',
    'ELAPSED_TIME': 'elapsed_time',
    'RECORDS': 'records',
    'GOAL_TIME': 'goal_time'
}

# 세션 업데이트
def update_session_view(request):
    if request.method == 'POST' or request.method == 'GET':  # GET 요청도 처리할 수 있도록 수정
        try:
            if request.method == 'POST':
                data = json.loads(request.body)
            else:
                data = request.GET
            # JSON 형식이 유효한지 확인
            if not all(key in data for key in TIMER_SESSION_KEYS.values()):
                return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
            # 세션 업데이트
            for key, value in data.items():
                request.session[TIMER_SESSION_KEYS[key]] = value
            return JsonResponse({'message': 'Session updated successfully.'})
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'error': 'Invalid data format.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


# 시간 문자열 시간으로 변환
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


# 뷰 함수
def test1_view(request):
    # 사용자가 세션에 로그인되어 있는지 확인
    if request.user.is_authenticated:
        # 세션에 로그인되어 있는 경우 사용자 이름을 세션에 저장
        request.session['session_username'] = request.user.username

        # Study_TimerSession 모델에서 모든 객체 가져오기
        sessions = Study_TimerSession.objects.all()
        
        # 기록을 timedelta 형식으로 변환
        for session in sessions:
            session.records = convert_to_timedelta(session.records)

        # 가장 높은 기록을 가진 객체 찾기
        highest_record = max(sessions, key=lambda session: convert_to_day(session.records))
        
        context = {
            'username': request.user.username,
            'sessions': sessions,
            'highest_record': highest_record
        }
    else:
        # 세션에 로그인되어 있지 않은 경우
        context = {'message': '로그인 되지 않았습니다.'}
    
    return render(request, 'user/test1.html', context)

# 테스트2 페이지 - 삭제예정
def test2_view(request):
    # 세션 데이터를 함께 전달
    context = {
        'timer_running': request.session.get('timer_running', False),
        'elapsed_time': request.session.get('elapsed_time', 0),
        'records': request.session.get('records', []),
        'goal_time': request.session.get('goal_time', 0)
    }
    return render(request, "user/test2.html", context)


# 타이머
def timer_view(request):
    context = {}
    return render(request, 'user/timer.html', context)


# 타이머 테스트화면 - 삭제예정
def timer_test1_view(request):
    context = {}
    return render(request, 'user/timer_test1.html', context)


# 서버에 타이머 기록 저장
def add_timer_view(request):
    if request.method == 'POST' or request.method == 'GET':
        # 폼에서 전송된 데이터 처리
        goal_time = request.POST.get('goal_time')
        elapsed_time = request.POST.get('elapsed_time')
        remaining_time = request.POST.get('remaining_time')
        goal_percent = request.POST.get('goal_percent')
        records = request.POST.get('records')

        print("User:", request.user)
        print("goal_time:", goal_time)
        print("elapsed_time:", elapsed_time)
        print("remaining_time:", remaining_time)
        print("goal_percent:", goal_percent)
        print("records:", records)
        # 모델에 저장
        timer_session = Study_TimerSession.objects.create(
            user=request.user,
            goal_time=goal_time,
            elapsed_time=elapsed_time,
            remaining_time=remaining_time,
            goalpercent=goal_percent,
            records=records
        )
        timer_session.save()
        
        return JsonResponse({'message': '성공적으로 저장하였습니다.'})
    else:
        return JsonResponse({'error': '저장 실패하였습니다.'}, status=400)
    

# 강의실 사이드 네비게이터 바
@login_required
def lecture_sidebar_view(request):
    user = request.user
    lecture_chapters = LectureChapter.objects.filter(user=user).select_related('lecture').order_by('lecture__title')

    lectures = []
    for chapter in lecture_chapters:
        lecture_title = chapter.lecture.title
        chapter_name = chapter.chapter_name
        lecture_url = reverse('user:lecture_detail', kwargs={'lecture_name': lecture_title})
        chapter_url = reverse('upload:chapter_detail', kwargs={'lecture_name': lecture_title, 'chapter_name': chapter_name})

        # 현재 강의가 lectures 리스트에 없으면 추가
        if not any(lecture['lecture'] == lecture_title for lecture in lectures):
            lectures.append({'lecture': lecture_title, 'chapters': []})

        # 현재 챕터 추가
        lectures[-1]['chapters'].append({'chapter_name': chapter_name, 'chapter_url': chapter_url, 'lecture_url': lecture_url})

    context = {
        'lectures': lectures,
    }
    return render(request, "user/lecture_sidebar.html", context)


# 챕터 삭제
@login_required
def delete_chapter(request, lecture_id, chapter_id):
    # 해당 강의와 챕터가 존재하는지 확인
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    chapter = get_object_or_404(LectureChapter, pk=chapter_id)

    # 챕터 삭제
    chapter.delete()
    print("챕터가 삭제되었습니다.")

    # 삭제 후 강의 상세 페이지로 리다이렉트
    return redirect('user:lecture_detail', lecture_name=lecture.title)
