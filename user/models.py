from django.contrib.auth.models import User
from django.db import models

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
    goal_time = models.TimeField()
    elapsed_time = models.TimeField()
    remaining_time = models.TimeField()
    records = models.TimeField()
    is_running = models.BooleanField(default=False)  # 타이머가 실행 중인지 여부
    is_stopped = models.BooleanField(default=True)  # 타이머가 중지되었는지 여부
    is_reset = models.BooleanField(default=True)  # 타이머가 초기화되었는지 여부

    def __str__(self):
        return f"사용자: {self.user.username}, 목표시간: {self.goal_time}, 지난시간: {self.elapsed_time}, 목표까지 남은시간: {self.remaining_time}, 기록: {self.records}, 실행여부: {self.is_running}, 중지여부: {self.is_stopped}, 초기화여부: {self.is_reset}"

    
    