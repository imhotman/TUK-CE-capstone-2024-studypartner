from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint
# from django.utils import timezone

class Lecture(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"강의명: {self.title}" 

class LectureChapter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # 사용자와의 외부 키 연결
    lecture = models.ForeignKey(Lecture, related_name='chapters', on_delete=models.CASCADE)
    chapter_name = models.CharField(max_length=100, null=True)  # 텍스트 형식의 챕터 이름 필드

    def __str__(self):
        return f"{self.lecture.title} - {self.chapter_name}"

    class Meta:
        verbose_name_plural = 'Lecture Chapters'

class Study_TimerSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    goal_time = models.CharField(max_length=100, null=True)
    elapsed_time = models.CharField(max_length=100, null=True)
    remaining_time = models.CharField(max_length=100, null=True)
    goalpercent = models.CharField(max_length=100, null=True)
    records = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return f"사용자: {self.user.username}, 날짜: {self.date},목표시간: {self.goal_time}, 지난시간: {self.elapsed_time}, 목표까지 남은시간: {self.remaining_time}, 목표달성률: {self.goalpercent},기록: {self.records}"

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['from_user', 'to_user'], name='unique_friend_requests')
        ]

    def __str__(self):
        return f"친구요청: {self.from_user.username}, 친구수락: {self.to_user.username}"

class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='friendships', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'friend'], name='unique_friendship')
        ]

    def __str__(self):
        return f"{self.user.username} 의 친구: {self.friend.username}"    


class UploadFile_handwriting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    chapter = models.ForeignKey(LectureChapter, on_delete=models.CASCADE, null=True)
    file_title = models.CharField(max_length=50, default="")
    file_name = models.FileField(null=True)

    def __str__(self):

        # return f"사용자={self.user}, 강의명={self.lecture}, 챕터명={self.chapter}, 파일 제목={self.file_title}, 파일 이름={self.file_name}"
        return f"사용자: {self.user}, 강의&챕터명: {self.chapter}, 파일 제목: {self.file_title}, 파일 이름: {self.file_name}"    