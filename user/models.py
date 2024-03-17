from django.contrib.auth.models import User
from django.db import models

class Lecture(models.Model):
    title = models.CharField(max_length=100)

class LectureChapter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # 사용자와의 외부 키 연결
    lecture = models.ForeignKey(Lecture, related_name='chapters', on_delete=models.CASCADE)
    chapter_name = models.CharField(max_length=100, null=True)  # 텍스트 형식의 챕터 이름 필드

    def __str__(self):
        return f"{self.lecture.title} - {self.chapter_name}"

    class Meta:
        verbose_name_plural = 'Lecture Chapters'