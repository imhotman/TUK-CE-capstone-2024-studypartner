from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, redirect
from django.contrib.auth.models import User
from user.models import Lecture, LectureChapter
from .models import UploadFile
from .forms import UploadFileForm  # UploadFileForm을 가져옴
from django.urls import reverse



# def chapter_detail_view(request, lecture_name, chapter_name):
#     # 강의명과 챕터명이 일치하는 LectureChapter 객체를 가져옴
#     chapter = LectureChapter.objects.filter(lecture__title=lecture_name, chapter_name=chapter_name).first()

#     # 현재 로그인한 사용자 정보를 가져옴
#     current_user = request.user

#     # LectureChapter가 없는 경우 404 에러 반환
#     if not chapter:
#         raise Http404("챕터를 찾을 수 없습니다.")

#     # 해당 챕터에 업로드된 파일들 가져오기
#     uploaded_files = UploadFile.objects.filter(chapter=chapter)

#     # 파일 업로드를 위한 폼 생성
#     form = UploadFileForm(request.POST or None, request.FILES or None)

#     context = {
#         'chapter': chapter,
#         'uploaded_files': uploaded_files,  # 업로드된 파일들을 context에 추가
#         'form': form,  # 폼을 context에 추가
#     }

#     return render(request, "upload/chapter_detail.html", context)



def chapter_detail_view(request, lecture_name=None, chapter_name=None):
    if lecture_name and chapter_name:
        # 강의명과 챕터명이 일치하는 LectureChapter 객체를 가져옴
        chapter = LectureChapter.objects.filter(lecture__title=lecture_name, chapter_name=chapter_name).first()

        # 현재 로그인한 사용자 정보를 가져옴
        current_user = request.user

        # LectureChapter가 없는 경우 404 에러 반환
        if not chapter:
            raise Http404("챕터를 찾을 수 없습니다.")

        # 해당 챕터에 업로드된 파일들 가져오기
        uploaded_files = UploadFile.objects.filter(chapter=chapter)

        # 파일 업로드를 위한 폼 생성
        form = UploadFileForm(request.POST or None, request.FILES or None)

        context = {
            'chapter': chapter,
            'uploaded_files': uploaded_files,  # 업로드된 파일들을 context에 추가
            'form': form,  # 폼을 context에 추가
        }

        return render(request, "upload/chapter_detail.html", context)
    else:
        # 이 부분은 lecture_view의 내용을 넣으면 됩니다.
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

        context = {
            'lectures': lectures,
        }
        return render(request, "user/lecture.html", context)

