from django.contrib import admin
from .models import Lecture, LectureChapter, Study_TimerSession

admin.site.register(Lecture)
admin.site.register(LectureChapter)
admin.site.register(Study_TimerSession)