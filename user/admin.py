from django.contrib import admin
from .models import Lecture, LectureChapter, Study_TimerSession, FriendRequest, Friendship

admin.site.register(Lecture)
admin.site.register(LectureChapter)
admin.site.register(Study_TimerSession)
# FriendRequest 모델 등록
@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'created_at']

# Friendship 모델 등록
@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ['user', 'friend', 'created_at']