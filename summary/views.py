from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, redirect
from django.contrib.auth.models import User
from user.models import Lecture, LectureChapter
from .models import UploadFile_summary
from .forms import UploadFile_summaryForm  # UploadFileForm을 가져옴

# Create your views here.


def summary_detail_view(request, lecture_name, chapter_name):
    # 강의명과 챕터명이 일치하는 LectureChapter 객체를 가져옴
    chapter = LectureChapter.objects.filter(lecture__title=lecture_name, chapter_name=chapter_name).first()

    # 현재 로그인한 사용자 정보를 가져옴
    current_user = request.user

    # LectureChapter가 없는 경우 404 에러 반환
    if not chapter:
        raise Http404("챕터를 찾을 수 없습니다.")

    # 해당 챕터에 업로드된 파일들 가져오기
    uploaded_files = UploadFile_summary.objects.filter(chapter=chapter)

    # 파일 업로드를 위한 폼 생성
    form = UploadFile_summaryForm(request.POST or None, request.FILES or None)

    context = {
        'chapter': chapter,
        'uploaded_files': uploaded_files,  # 업로드된 파일들을 context에 추가
        'form': form,  # 폼을 context에 추가
    }

    return render(request, "summary/summary_detail.html", context)



def upload_file_summary(request, lecture_name, chapter_name):
    try:
        chapter = LectureChapter.objects.get(lecture__title=lecture_name, chapter_name=chapter_name)
    except LectureChapter.DoesNotExist:
        raise Http404("챕터를 찾을 수 없습니다.")
    
    if request.method == 'POST':
        form = UploadFile_summaryForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = form.save(commit=False)
            upload_file.chapter = chapter
            upload_file.user = request.user
            upload_file.save()
            return redirect('summary:summary_detail', lecture_name=lecture_name, chapter_name=chapter_name)
    else:
        form = UploadFile_summaryForm()
    
    context = {
        'chapter': chapter,
        'form': form
    }
    return render(request, "summary/summary_detail.html", context)
