from django.contrib import admin
from .models import PrivateChatRoom, PrivateMessage

# PrivateChatRoom 모델을 관리할 관리자 클래스
class PrivateChatRoomAdmin(admin.ModelAdmin):
    # 관리자 페이지에서 보여줄 필드
    list_display = ('user1', 'user2')
    # 관리자 페이지에서 검색할 필드
    search_fields = ('user1__username', 'user2__username')
    # 관리자 페이지에서 필터링할 필드
    list_filter = ('user1', 'user2')

# PrivateMessage 모델을 관리할 관리자 클래스
class PrivateMessageAdmin(admin.ModelAdmin):
    # 관리자 페이지에서 보여줄 필드
    list_display = ('chat_room', 'sender', 'receiver', 'content', 'file', 'timestamp', 'is_read')
    # 관리자 페이지에서 검색할 필드
    search_fields = ('sender__username', 'receiver__username', 'content')
    # 관리자 페이지에서 필터링할 필드
    list_filter = ('sender', 'receiver', 'chat_room', 'is_read')
    # 관리자 페이지에서 필드 순서 지정
    ordering = ('-timestamp',)  # 최근 메시지부터 정렬

# 모델을 관리자 사이트에 등록
admin.site.register(PrivateChatRoom, PrivateChatRoomAdmin)
admin.site.register(PrivateMessage, PrivateMessageAdmin)