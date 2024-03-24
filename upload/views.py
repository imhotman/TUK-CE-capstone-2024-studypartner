from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, redirect
from django.contrib.auth.models import User
from user.models import LectureChapter
from .models import UploadFile
from .forms import UploadFileForm  # UploadFileForm을 가져옴



def chapter_detail_view(request, lecture_name, chapter_name):
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













@login_required
def upload_file(request, lecture_name, chapter_name):
    # 강의명과 챕터명이 일치하는 LectureChapter 객체를 가져옴
    chapter = LectureChapter.objects.filter(lecture__title=lecture_name, chapter_name=chapter_name).first()

    # LectureChapter가 없는 경우 404 에러 반환
    if not chapter:
        raise Http404("챕터를 찾을 수 없습니다.")

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # 업로드된 파일의 lecture 필드를 해당 챕터의 강의로 설정
            upload_file = form.save(commit=False)
            upload_file.chapter = chapter

            # 현재 로그인한 사용자 정보를 가져와서 업로드 파일의 user 필드에 설정
            upload_file.user = request.user
            
            upload_file.save()

            # 파일 업로드 성공 시 해당 챕터 세부 정보 페이지로 리디렉션
            print("파일 업로드 성공하였습니다.")
            return redirect('upload:chapter_detail', lecture_name=lecture_name, chapter_name=chapter_name)
        
    # 파일 업로드 실패 시 현재 페이지를 다시 렌더링하여 업로드 폼을 표시
    print("파일 업로드 실패하였습니다.")
    context = {
        'chapter': chapter,
        'form': UploadFileForm()  # 업로드 폼 생성
    }
    print("모두 실패")
    return render(request, "upload/chapter_detail.html", context)
