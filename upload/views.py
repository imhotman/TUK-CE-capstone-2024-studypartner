from django.shortcuts import render, redirect, Http404
from .models import User, LectureChapter
# Create your views here.

def chapter_detail_view(request, lecture_name, chapter_name):
    # 강의명과 챕터명이 일치하는 LectureChapter 객체를 가져옴
    chapter = LectureChapter.objects.filter(lecture__title=lecture_name, chapter_name=chapter_name).first()

    # LectureChapter가 없는 경우 404 에러 반환
    if not chapter:
        raise Http404("챕터를 찾을 수 없습니다.")

    # 강의에 대한 추가적인 정보를 가져오거나 생성하는 코드 작성

    context = {
        'chapter': chapter,
        # 챕터에 관련된 다른 정보를 추가할 수 있음
    }

    return render(request, "upload/chapter_detail.html", context)


