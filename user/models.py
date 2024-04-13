from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

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

    
    