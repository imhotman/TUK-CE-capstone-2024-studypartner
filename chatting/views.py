from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Lecture, LectureChapter, Study_TimerSession, UploadFile_handwriting
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from .models import Study_TimerSession, FriendRequest, Friendship
from .models import PrivateChatRoom, PrivateMessage
from datetime import datetime, timedelta, date
import json
from django.utils import timezone
import pytz
import locale
from datetime import datetime


# locale 설정
locale.setlocale(locale.LC_TIME, 'ko_KR.UTF-8')


# timestamp 시간 형식 변경
def format_timestamp(timestamp):
    return timestamp.strftime('%Y. %m. %d. %p %I:%M:%S').replace('AM', '오전').replace('PM', '오후')


# 채팅시스템
@login_required
def private_chat_room(request, user_id):
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


    current_user = request.user
    other_user = get_object_or_404(User, id=user_id)

    # 채팅방 생성 또는 가져오기
    chat_room, created = get_or_create_chat_room(current_user, other_user)
    
    # 읽지 않은 메시지를 읽은 상태로 업데이트
    unread_messages = PrivateMessage.objects.filter(chat_room=chat_room, receiver=current_user, is_read=False)
    unread_messages.update(is_read=True)
    
    # 기존 메시지를 가져오기
    messages = PrivateMessage.objects.filter(chat_room=chat_room).order_by('timestamp')

    context = {
        'request_user': user,
        'friend_requests': friend_requests,
        'friends': friends,
        'lectures': lectures,
        'today_record': today_record,  # today_record를 context에 포함
        'friends_records': friends_records,
        'user_id': user_id,
        'unread_messages': unread_messages.count(),
        'created': created,
        'room_name': user_id,  # WebSocket과 연결하기 위한 방 이름
        'current_user': current_user,
        'other_user': other_user,
        'messages': messages  # 기존 메시지를 컨텍스트에 추가
    }
    
    return render(request, "chatting/chatting_test.html", context)



# 시간 문자열 시간으로 변환
def convert_to_timedelta(record):
    # 시간 문자열을 ':'로 분할하여 시, 분, 초를 추출
    hours, minutes, seconds = map(int, record.split(':'))
    # timedelta 객체로 변환하여 반환
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)



# def private_chat_room(request, user_id):
    
#     current_user = request.user
#     other_user = get_object_or_404(User, id=user_id)
    
#     # 채팅방 생성 또는 가져오기
#     chat_room, created = PrivateChatRoom.objects.get_or_create(
#         user1=request.user if request.user.id < other_user.id else other_user,
#         user2=other_user if request.user.id < other_user.id else request.user
#     )
    
#     # 읽지 않은 메시지를 읽은 상태로 업데이트
#     unread_messages = PrivateMessage.objects.filter(chat_room=chat_room, receiver=request.user, is_read=False)
#     unread_messages.update(is_read=True)

#     # 템플릿에 전달할 context
#     context = {
#         'user_id': user_id,
#         'unread_messages': unread_messages.count(),
#         'created': created,  # 채팅방이 새로 생성되었는지 여부를 context에 추가
#         'room_name': chat_room.id,  # WebSocket과 연결하기 위한 방 이름
#         'current_user' : current_user,
#         'other_user' : other_user
#     }
    
#     return render(request, 'chatting/chatting_room.html', context)




# def private_chat_room(request, user_id):
#     current_user = request.user
#     other_user = get_object_or_404(User, id=user_id)
    
#     # 채팅방 생성 또는 가져오기
#     chat_room, created = PrivateChatRoom.objects.get_or_create(
#         user1=current_user if current_user.id < other_user.id else other_user,
#         user2=other_user if current_user.id < other_user.id else current_user
#     )
    
#     # 읽지 않은 메시지를 읽은 상태로 업데이트
#     unread_messages = PrivateMessage.objects.filter(chat_room=chat_room, receiver=current_user, is_read=False)
#     unread_messages.update(is_read=True)

#     context = {
#         'user_id': user_id,
#         'unread_messages': unread_messages.count(),
#         'created': created,
#         'room_name': user_id,  # WebSocket과 연결하기 위한 방 이름
#         'current_user': current_user,
#         'other_user': other_user
#     }
    
#     return render(request, 'chatting/chatting_room.html', context)


# 채팅방 생성 또는 가져오는 함수
def get_or_create_chat_room(user1, user2):
    chat_room, created = PrivateChatRoom.objects.get_or_create(
        user1=min(user1, user2, key=lambda x: x.id),
        user2=max(user1, user2, key=lambda x: x.id)
    )
    return chat_room, created


# 채팅방
def chatting_test_view(request, user_id):
    current_user = request.user
    other_user = get_object_or_404(User, id=user_id)
    
    # 채팅방 생성 또는 가져오기
    chat_room, created = get_or_create_chat_room(current_user, other_user)
    
    # 읽지 않은 메시지를 읽은 상태로 업데이트
    unread_messages = PrivateMessage.objects.filter(chat_room=chat_room, receiver=current_user, is_read=False)
    unread_messages.update(is_read=True)
    
    # 기존 메시지를 가져오기
    messages = PrivateMessage.objects.filter(chat_room=chat_room).order_by('timestamp')
    
    context = {
        'user_id': user_id,
        'unread_messages': unread_messages.count(),
        'created': created,
        'room_name': user_id,  # WebSocket과 연결하기 위한 방 이름
        'current_user': current_user,
        'other_user': other_user,
        'messages': messages  # 기존 메시지를 컨텍스트에 추가
    }
    
    return render(request, 'chatting/chatting_room.html', context)


# 채팅 삭제
# def delete_message(request):
#     message_id = request.POST.get('message_id')
#     try:
#         message = PrivateMessage.objects.get(id=message_id, sender=request.user)
#         message.delete()
#         return JsonResponse({'status': 'success'})
#     except PrivateMessage.DoesNotExist:
#         return JsonResponse({'status': 'error', 'message': 'Message not found or not authorized'})


