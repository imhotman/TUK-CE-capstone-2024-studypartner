from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Lecture, LectureChapter, Study_TimerSession, UploadFile_handwriting
from django.contrib.auth.decorators import login_required
from .forms import LectureChapterForm, UploadFile_handwritingForm
from django.urls import reverse
from django.http import JsonResponse
from .models import Study_TimerSession, FriendRequest, Friendship
from datetime import datetime, timedelta, date
import json
from django.utils import timezone
import pytz



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


    # 현재 사용자의 친구 요청 가져오기
    friend_requests = FriendRequest.objects.filter(to_user=request.user)

    # 현재 사용자의 친구 목록 가져오기
    user = request.user
    friends = Friendship.objects.filter(user=user).select_related('friend')

    # 오늘의 날짜 범위 계산
    user_timezone = pytz.timezone('Asia/Seoul')  # 사용자의 시간대로 설정
    today = timezone.now().astimezone(user_timezone).date()
    start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    end_of_day = start_of_day + timedelta(days=1)

    # 현재 사용자의 모든 공부 세션 가져오기 (날짜 역순 정렬)
    sessions = Study_TimerSession.objects.filter(user=request.user).order_by('-date')

    # 기록을 timedelta 형식으로 변환
    for session in sessions:
        session.records = convert_to_timedelta(session.records)

    # 오늘의 기록 가져오기 (가장 높은 기록)
    today_sessions = sessions.filter(date__date=today)
    today_record_value = None
    today_record = None  # today_record 변수를 미리 정의
    if today_sessions:
        today_record = max(today_sessions, key=lambda session: session.records)
        today_record_value = convert_to_timedelta(today_record.records)  # timedelta로 변환

    # 친구들의 오늘의 공부 기록 가져오기
    friends_records = []
    for friendship in friends:
        friend = friendship.friend
        friend_today_sessions = Study_TimerSession.objects.filter(user=friend, date__range=(start_of_day, end_of_day))

        if friend_today_sessions:
            best_record = max(friend_today_sessions, key=lambda session: session.records)
            friends_records.append((friend.username, convert_to_timedelta(best_record.records)))

    # 나의 기록을 friends_records에 추가
    if today_record_value:
        friends_records.append((user.username, today_record_value))

    # 기록을 기준으로 내림차순 정렬
    friends_records.sort(key=lambda x: x[1], reverse=True)

    context = {
        'request_user': user,
        'friend_requests': friend_requests,
        'friends': friends,
        'lectures': lectures,
        'today_record': today_record,  # today_record를 context에 포함
        'friends_records': friends_records,
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
    
    # 현재 사용자의 친구 요청 가져오기
    friend_requests = FriendRequest.objects.filter(to_user=request.user)

    # 현재 사용자의 친구 목록 가져오기
    user = request.user
    friends = Friendship.objects.filter(user=user).select_related('friend')

    # 오늘의 날짜 범위 계산
    user_timezone = pytz.timezone('Asia/Seoul')  # 사용자의 시간대로 설정
    today = timezone.now().astimezone(user_timezone).date()
    start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    end_of_day = start_of_day + timedelta(days=1)

    # 현재 사용자의 모든 공부 세션 가져오기 (날짜 역순 정렬)
    sessions = Study_TimerSession.objects.filter(user=request.user).order_by('-date')

    # 기록을 timedelta 형식으로 변환
    for session in sessions:
        session.records = convert_to_timedelta(session.records)

    # 오늘의 기록 가져오기 (가장 높은 기록)
    today_sessions = sessions.filter(date__date=today)
    today_record_value = None
    today_record = None  # today_record 변수를 미리 정의
    if today_sessions:
        today_record = max(today_sessions, key=lambda session: session.records)
        today_record_value = convert_to_timedelta(today_record.records)  # timedelta로 변환

    # 친구들의 오늘의 공부 기록 가져오기
    friends_records = []
    for friendship in friends:
        friend = friendship.friend
        friend_today_sessions = Study_TimerSession.objects.filter(user=friend, date__range=(start_of_day, end_of_day))

        if friend_today_sessions:
            best_record = max(friend_today_sessions, key=lambda session: session.records)
            friends_records.append((friend.username, convert_to_timedelta(best_record.records)))

    # 나의 기록을 friends_records에 추가
    if today_record_value:
        friends_records.append((user.username, today_record_value))

    # 기록을 기준으로 내림차순 정렬
    friends_records.sort(key=lambda x: x[1], reverse=True)

    

    context = {
        'lecture_name': lecture_name,
        'lecture_chapters': lecture_chapters,
        'lectures': lectures,
        'request_user': user,
        'friend_requests': friend_requests,
        'friends_records': friends_records,
        'friends': friends,
        'today_record': today_record
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
# def friend_record_view(request):
#     # 현재 사용자의 친구 요청 가져오기
#     friend_requests = FriendRequest.objects.filter(to_user=request.user)

#     # 현재 사용자의 친구 목록 가져오기
#     user = request.user
#     friends = Friendship.objects.filter(user=user).select_related('friend')

#     # 오늘의 날짜 범위 계산
#     today = timezone.now().date()
#     start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()))
#     end_of_day = start_of_day + timedelta(days=1)

#     # 친구들의 오늘의 공부 기록 가져오기
#     friends_records = []
#     for friendship in friends:
#         friend = friendship.friend
#         today_sessions = Study_TimerSession.objects.filter(user=friend, date__range=(start_of_day, end_of_day))
#         if today_sessions:
#             best_record = max(today_sessions, key=lambda session: session.records)
#             friends_records.append((friend.username, best_record.records))

#     context = {
#         'request_user': user,
#         'friend_requests': friend_requests,
#         'friends': friends,
#         'friends_records': friends_records,
#     }
    
#     return render(request, 'user/friend.html', context)


def friend_record_view(request):
    if not request.user.is_authenticated:
        return render(request, 'user/friend.html', {'message': '로그인 되지 않았습니다.'})

    # 현재 사용자의 친구 요청 가져오기
    friend_requests = FriendRequest.objects.filter(to_user=request.user)

    # 현재 사용자의 친구 목록 가져오기
    user = request.user
    friends = Friendship.objects.filter(user=user).select_related('friend')

    # 오늘의 날짜 범위 계산
    user_timezone = pytz.timezone('Asia/Seoul')  # 사용자의 시간대로 설정
    today = timezone.now().astimezone(user_timezone).date()
    start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    end_of_day = start_of_day + timedelta(days=1)

    # 현재 사용자의 모든 공부 세션 가져오기 (날짜 역순 정렬)
    sessions = Study_TimerSession.objects.filter(user=request.user).order_by('-date')

    # 기록을 timedelta 형식으로 변환
    for session in sessions:
        session.records = convert_to_timedelta(session.records)

    # 오늘의 기록 가져오기 (가장 높은 기록)
    today_sessions = sessions.filter(date__date=today)
    print(today_sessions)
    today_record_value = None
    today_record = None
    if today_sessions:
        today_record = max(today_sessions, key=lambda session: session.records)
        today_record_value = convert_to_timedelta(today_record.records)  # timedelta로 변환

    # 친구들의 오늘의 공부 기록 가져오기
    friends_records = []
    for friendship in friends:
        friend = friendship.friend
        friend_today_sessions = Study_TimerSession.objects.filter(user=friend, date__range=(start_of_day, end_of_day))

        if friend_today_sessions:
            best_record = max(friend_today_sessions, key=lambda session: session.records)
            friends_records.append((friend.username, convert_to_timedelta(best_record.records)))

    # 나의 기록을 friends_records에 추가
    if today_record_value:
        friends_records.append((user.username, today_record_value))

    # 기록을 기준으로 내림차순 정렬
    friends_records.sort(key=lambda x: x[1], reverse=True)

    context = {
        'request_user': user,
        'friend_requests': friend_requests,
        'friends_records': friends_records,
        'today_record': today_record,
    }

    return render(request, 'user/friend_record.html', context)





# 오늘의 공부기록 페이지
def today_records_view(request):
    # 세션 데이터를 함께 전달
    if request.user.is_authenticated:
        # 현재 사용자의 모든 공부 세션 가져오기 (날짜 역순 정렬)
        sessions = Study_TimerSession.objects.filter(user=request.user).order_by('-date')

        # 기록을 timedelta 형식으로 변환
        for session in sessions:
            session.records = convert_to_timedelta(session.records)

        # 한국 시간대로 변환
        korea_tz = pytz.timezone('Asia/Seoul')
        for session in sessions:
            session.date = session.date.astimezone(korea_tz)

        # 오늘의 기록 가져오기 (가장 높은 기록)
        today = date.today()
        today_sessions = sessions.filter(date__date=today)
        if today_sessions:
            today_record = max(today_sessions, key=lambda session: session.records)
        else:
            today_record = None

        context = {
            'sessions': sessions,
            'today_record': today_record,
        }

    else:
        context = {'message': '로그인 되지 않았습니다.'}
    
    return render(request, 'user/today_records.html', context)



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


# # 강의 삭제
# @login_required
# def delete_lecture_view(request):
#     if request.method == 'POST':
#         lecture_title = request.POST.get('lecture_title')
#         lecture = get_object_or_404(Lecture, title=lecture_title)
        
#         # Lecture와 연결된 모든 LectureChapter가 자동으로 삭제됨
#         lecture.delete()
#         print("강의와 챕터가 삭제되었습니다.")
    
#     # 강의 삭제 후 사이드바 페이지로 리다이렉트
#     return redirect('user:lecture')

# 강의 삭제
@login_required
def delete_lecture_view(request):
    if request.method == 'POST':
        lecture_title = request.POST.get('lecture_title')
        try:
            lecture = get_object_or_404(Lecture, title=lecture_title)
            # Lecture와 연결된 모든 LectureChapter가 자동으로 삭제됨
            lecture.delete()
            print("강의와 챕터가 삭제되었습니다.")
            return JsonResponse({'success': True})
        except Lecture.DoesNotExist:
            return JsonResponse({'success': False, 'error': '강의를 찾을 수 없습니다.'})
        except Exception as e:
            print(f"삭제 중 오류 발생: {e}")
            return JsonResponse({'success': False, 'error': '강의 삭제 중 오류가 발생했습니다.'})
    
    # POST가 아닐 경우
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


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



# 친구 요청
def send_friend_request(request):
    if request.method == 'POST':
        from_user = request.user
        friend_id = request.POST.get('friend_id')
        print(from_user)
        print(friend_id)

        try:
            friend_user = User.objects.get(username=friend_id)
            
            # 동일한 사용자인지 확인
            if friend_user == request.user:
                print("동일한 사용자입니다.")
                return redirect('user:lecture')
            
            # 이미 친구인지 또는 이미 요청을 보낸 경우인지 확인
            if Friendship.objects.filter(user=request.user, friend=friend_user).exists() or FriendRequest.objects.filter(from_user=request.user, to_user=friend_user).exists():
                print("이미 친구이거나 요청을 보낸 사용자입니다.")
                return redirect('user:lecture')
            
            # 친구 요청 생성 및 저장
            friend_request = FriendRequest.objects.create(from_user=request.user, to_user=friend_user)
            print("친구 요청 완료")
            return redirect('user:lecture')  # 요청을 보낸 후 홈 페이지로 리다이렉트
            
        except User.DoesNotExist:
            pass
    # POST 요청이 아니거나 요청 수신자가 잘못된 경우
    print("친구 요청 에러")
    return redirect('user:lecture')  # 에러 페이지로 리다이렉트
    



# 친구 시스템 사이트 뷰
def friend_view(request):
    # 현재 사용자의 친구 요청 가져오기
    friend_requests = FriendRequest.objects.filter(to_user=request.user)

    # 현재 사용자의 친구 목록 가져오기
    user = request.user
    friends = Friendship.objects.filter(user=user).select_related('friend')

    context = {
        'request_user': user,
        'friend_requests': friend_requests,
        'friends': friends,
        }
    
    return render(request, 'user/friend.html', context)


# def accept_friend_request(request_id):
#     try:
#         friend_request = FriendRequest.objects.get(id=request_id)
#         user1 = friend_request.from_user
#         user2 = friend_request.to_user
        
#         # 친구 관계 생성(친구 추가)
#         Friendship.objects.create(user=user1, friend=user2)
#         Friendship.objects.create(user=user2, friend=user1)
        
#         # 친구 요청 삭제
#         friend_request.delete()
        
#     except FriendRequest.DoesNotExist:
#         pass

#     return redirect('user:friend')  # 이동할 URL을 설정해야 합니다.


# 친구 요청 수락
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    
    # 이미 친구인지 확인
    if Friendship.objects.filter(user=friend_request.to_user, friend=friend_request.from_user).exists():
        # 이미 친구인 경우에는 요청을 수락할 필요가 없으므로 리다이렉트
        return redirect('user:lecture')
    
    # 친구 관계 생성(친구 추가)
    Friendship.objects.create(user=friend_request.from_user, friend=friend_request.to_user)
    Friendship.objects.create(user=friend_request.to_user, friend=friend_request.from_user)
    
    # 친구 요청 삭제
    friend_request.delete()
    
    return redirect('user:lecture')  # 친구 요청을 수락한 후에는 리다이렉트


# 친구 삭제
def delete_friend(request, friend_id):
    # 친구 관계 가져오기
    friendship = get_object_or_404(Friendship, user=request.user, friend_id=friend_id)
    # 역방향 친구 관계 가져오기
    reverse_friendship = get_object_or_404(Friendship, user=friend_id, friend=request.user)
    
    # 친구 관계 삭제
    friendship.delete()
    reverse_friendship.delete()
    
    return redirect('user:lecture')


# 친구 요청 거절
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    friend_request.delete()
    return redirect('user:lecture')















# 손글씨 제작 테스트 페이지
def handwriting_view(request, lecture_name, chapter_name):
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

    # 해당 챕터에 업로드된 파일들 가져오기
    uploaded_files = UploadFile_handwriting.objects.filter(chapter=chapter)

    # 파일 업로드를 위한 폼 생성
    form = UploadFile_handwritingForm(request.POST or None, request.FILES or None)    

    # 현재 사용자의 친구 요청 가져오기
    friend_requests = FriendRequest.objects.filter(to_user=request.user)

    # 현재 사용자의 친구 목록 가져오기
    user = request.user
    friends = Friendship.objects.filter(user=user).select_related('friend')

    # 오늘의 날짜 범위 계산
    user_timezone = pytz.timezone('Asia/Seoul')  # 사용자의 시간대로 설정
    today = timezone.now().astimezone(user_timezone).date()
    start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    end_of_day = start_of_day + timedelta(days=1)

    # 현재 사용자의 모든 공부 세션 가져오기 (날짜 역순 정렬)
    sessions = Study_TimerSession.objects.filter(user=request.user).order_by('-date')

    # 기록을 timedelta 형식으로 변환
    for session in sessions:
        session.records = convert_to_timedelta(session.records)

    # 오늘의 기록 가져오기 (가장 높은 기록)
    today_sessions = sessions.filter(date__date=today)
    today_record_value = None
    today_record = None  # today_record 변수를 미리 정의
    if today_sessions:
        today_record = max(today_sessions, key=lambda session: session.records)
        today_record_value = convert_to_timedelta(today_record.records)  # timedelta로 변환

    # 친구들의 오늘의 공부 기록 가져오기
    friends_records = []
    for friendship in friends:
        friend = friendship.friend
        friend_today_sessions = Study_TimerSession.objects.filter(user=friend, date__range=(start_of_day, end_of_day))

        if friend_today_sessions:
            best_record = max(friend_today_sessions, key=lambda session: session.records)
            friends_records.append((friend.username, convert_to_timedelta(best_record.records)))

    # 나의 기록을 friends_records에 추가
    if today_record_value:
        friends_records.append((user.username, today_record_value))

    # 기록을 기준으로 내림차순 정렬
    friends_records.sort(key=lambda x: x[1], reverse=True)

    context = {
        'chapter': chapter,
        'lectures': lectures,
        'chapter_name': chapter_name,
        'uploaded_files': uploaded_files,  # 업로드된 파일들을 context에 추가
        'form': form,  # 폼을 context에 추가
        'request_user': user,
        'friend_requests': friend_requests,
        'friends_records': friends_records,
        'friends': friends,
        'today_record': today_record
        }

    return render(request, "user/handwriting.html", context)


def upload_file_handwriting(request, lecture_name, chapter_name):
    try:
        chapter = LectureChapter.objects.get(lecture__title=lecture_name, chapter_name=chapter_name)
    except LectureChapter.DoesNotExist:
        raise Http404("챕터를 찾을 수 없습니다.")
    
    if request.method == 'POST':
        form = UploadFile_handwritingForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = form.save(commit=False)
            upload_file.chapter = chapter
            upload_file.user = request.user
            upload_file.save()
            return redirect('user:handwriting', lecture_name=lecture_name, chapter_name=chapter_name)
    else:
        form = UploadFile_handwritingForm()
    
    context = {
        'chapter': chapter,
        'form': form
    }
    return render(request, "user/handwriting.html", context)


def delete_file_handwriting(request, file_id):
    file_to_delete = get_object_or_404(UploadFile_handwriting, id=file_id)
    lecture_name = file_to_delete.chapter.lecture.title
    chapter_name = file_to_delete.chapter.chapter_name
    file_to_delete.delete()
    return redirect('user:handwriting', lecture_name=lecture_name, chapter_name=chapter_name)


### 공부기록을 볼 수 있는 페이지 및 함수들 ###
def study_recordpage_view(request):
    user = request.user

    # 사용자의 챕터 목록 가져오기
    lecture_chapters = LectureChapter.objects.filter(user=user).select_related('lecture').order_by('lecture__title')
    lectures = organize_lectures(lecture_chapters)

    # 친구 요청 및 친구 목록 가져오기
    friend_requests = FriendRequest.objects.filter(to_user=user)
    friends = Friendship.objects.filter(user=user).select_related('friend')

    # 오늘의 기록 및 친구들의 기록 가져오기
    today_record, friends_records = get_today_and_friends_records(user, friends)

    # 내 모든 공부 세션 및 각 날짜별로 가장 높은 기록 가져오기
    sessions, highest_records = get_user_sessions(user)

    # 템플릿에 전달할 context 생성
    context = {
        'sessions': sessions,
        'highest_records': highest_records,
        'request_user': user,
        'friend_requests': friend_requests,
        'friends': friends,
        'lectures': lectures,
        'today_record': today_record,
        'friends_records': friends_records,
    }

    if not request.user.is_authenticated:
        context = {'message': '로그인 되지 않았습니다.'}

    return render(request, 'user/study_recordpage.html', context)

def organize_lectures(lecture_chapters):
    lectures = []
    for chapter in lecture_chapters:
        lecture_title = chapter.lecture.title
        chapter_name = chapter.chapter_name
        chapter_url = reverse('upload:chapter_detail', kwargs={'lecture_name': lecture_title, 'chapter_name': chapter_name})

        if not any(lecture['lecture'] == lecture_title for lecture in lectures):
            lectures.append({'lecture': lecture_title, 'chapters': []})

        lectures[-1]['chapters'].append({'chapter_name': chapter_name, 'chapter_url': chapter_url})
    return lectures

def get_today_and_friends_records(user, friends):
    user_timezone = pytz.timezone('Asia/Seoul')
    today = timezone.now().astimezone(user_timezone).date()

    start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    end_of_day = start_of_day + timedelta(days=1)

    sessions = Study_TimerSession.objects.filter(user=user).order_by('-date')
    today_sessions = sessions.filter(date__date=today)
    
    today_record = max(today_sessions, key=lambda session: session.records, default=None)
    today_record_value = convert_to_timedelta(today_record.records) if today_record else None

    friends_records = []
    for friendship in friends:
        friend = friendship.friend
        friend_today_sessions = Study_TimerSession.objects.filter(user=friend, date__range=(start_of_day, end_of_day))
        if friend_today_sessions:
            best_record = max(friend_today_sessions, key=lambda session: session.records)
            friends_records.append((friend.username, convert_to_timedelta(best_record.records)))

    if today_record_value:
        friends_records.append((user.username, today_record_value))
    
    friends_records.sort(key=lambda x: x[1], reverse=True)
    
    return today_record, friends_records

def get_user_sessions(user):
    sessions = Study_TimerSession.objects.filter(user=user).order_by('-date')
    korea_tz = pytz.timezone('Asia/Seoul')
    
    for session in sessions:
        session.date = session.date.astimezone(korea_tz)
        session.records = convert_to_timedelta(session.records)
    
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
            elif convert_to_day(session.records) > convert_to_day(highest_record.records):
                highest_record = session
        highest_records.append(highest_record)
    
    return sessions, highest_records

### 공부기록을 볼 수 있는 페이지 및 함수들 끝 ###

