from django.shortcuts import render, Http404
from django.contrib.auth.models import User
from user.models import LectureChapter
from .forms import UploadFileForm  # UploadFileForm을 가져옴

def chapter_detail_view(request, lecture_name, chapter_name):
    # 강의명과 챕터명이 일치하는 LectureChapter 객체를 가져옴
    chapter = LectureChapter.objects.filter(lecture__title=lecture_name, chapter_name=chapter_name).first()

    # LectureChapter가 없는 경우 404 에러 반환
    if not chapter:
        raise Http404("챕터를 찾을 수 없습니다.")

    # UploadFileForm 인스턴스 생성
    form = UploadFileForm()

    context = {
        'chapter': chapter,
        'form': form,  # UploadFileForm을 context에 추가
    }

    return render(request, "upload/chapter_detail.html", context)


