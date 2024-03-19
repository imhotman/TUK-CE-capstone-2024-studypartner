from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Lecture, LectureChapter
from django.contrib.auth.decorators import login_required
from .forms import LectureChapterForm

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(username=username, password=password)

        if user is not None:
            print("로그인 성공")
            messages.success(request, "로그인 성공!")
            login(request, user)
            return redirect("index")  # 로그인 성공 시 index 페이지로 리다이렉트
        else:
            messages.error(request, "로그인 실패")
            print("로그인 실패")

    return render(request, "user/login.html")

def logout_view(request):
    logout(request)
    print("로그아웃")
    return redirect("index")

def signup_view(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "회원가입 성공!")
        print("회원가입 성공")
        return redirect("signup_done")

    return render(request, "user/signup.html")






# @login_required
# def lecture_list_view(request):
#     user = request.user  # 현재 로그인한 사용자 정보 가져오기
#     chapters = LectureChapter.objects.filter(user=user)

#     context = {
#         'chapters': chapters,  # 사용자의 LectureChapter 객체 목록을 전달
#     }

#     return render(request, "user/lecture_list.html", context)



from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import LectureChapter

@login_required
def lecture_list_view(request):
    user = request.user
    lecture_chapters = LectureChapter.objects.filter(user=user).select_related('lecture').order_by('lecture__title')

    lectures = []
    current_lecture = None
    for chapter in lecture_chapters:
        if current_lecture != chapter.lecture.title:
            lectures.append({'lecture': chapter.lecture.title, 'chapters': []})
            current_lecture = chapter.lecture.title
        # 각 챕터에 대한 URL을 생성하여 추가
        kwargs={'lecture_name': chapter.lecture.title, 'chapter_name': chapter.chapter_name}    
        chapter_url = reverse('chapter_detail', kwargs=kwargs )
        lectures[-1]['chapters'].append({'chapter_name': chapter.chapter_name, 'chapter_url': chapter_url}) 

    context = {
        'lectures': lectures,
    }
    return render(request, "user/lecture_list.html", context)











# @login_required
# def lecture_view(request):
#     user = request.user  # 현재 로그인한 사용자 정보 가져오기
#     chapters = LectureChapter.objects.filter(user=user)

#     context = {
#         'chapters': chapters,  # 사용자의 LectureChapter 객체 목록을 전달
#     }

#     return render(request, "user/lecture.html", context)

@login_required
def lecture_view(request):
    user = request.user
    lecture_chapters = LectureChapter.objects.filter(user=user).select_related('lecture').order_by('lecture__title')

    lectures = []
    current_lecture = None
    for chapter in lecture_chapters:
        if current_lecture != chapter.lecture.title:
            lectures.append({'lecture': chapter.lecture.title, 'chapters': []})
            current_lecture = chapter.lecture.title
        lectures[-1]['chapters'].append(chapter.chapter_name)

    context = {
        'lectures': lectures,
    }
    return render(request, "user/lecture.html", context)











# @login_required
# def add_lecture_chapter_view(request):
#     if request.method == 'POST':
#         form = LectureChapterForm(request.POST)
#         if form.is_valid():
#             # 폼에서 입력한 데이터 가져오기
#             lecture_name = form.cleaned_data.get('lecture_name')
#             chapter_name = form.cleaned_data.get('chapter_name')
            
#             # 터미널에 출력
#             print("User:", request.user)
#             print("Lecture:", lecture_name)
#             print("Chapter Name:", chapter_name)
#             print("성공적으로 추가되었습니다.")

#             # Lecture 모델에서 해당 강의를 가져오거나 생성
#             lecture, created = Lecture.objects.get_or_create(title=lecture_name)

#             # 새로운 LectureChapter 객체 생성 및 저장
#             chapter = form.save(commit=False)
#             chapter.user = request.user
#             chapter.lecture = lecture  # Lecture 객체 할당
#             chapter.save()

#             messages.success(request, '강의 챕터가 성공적으로 추가되었습니다.')
#             return render(request, "user/add_lecture_chapter.html")
#     else:
#         form = LectureChapterForm()

#     # 폼 유효성 검사 실패 시에도 폼과 함께 에러 메시지를 전달
#     if form.errors:
#         # 폼에서 입력한 데이터 가져오기
#         lecture_name = form.cleaned_data.get('lecture_name')
#         chapter_name = form.cleaned_data.get('chapter_name')
        
#         # 터미널에 출력
#         print("User:", request.user)
#         print("Lecture:", lecture_name)
#         print("Chapter Name:", chapter_name)
#         print("강의 챕터 추가에 실패했습니다.")

#         messages.error(request, '강의 챕터 추가에 실패했습니다. 입력을 다시 확인해주세요.')

#     return render(request, 'user/add_lecture_chapter.html')







@login_required
def add_lecture_chapter_view(request):
    if request.method == 'POST':
        form = LectureChapterForm(request.POST)
        if form.is_valid():
            # 폼에서 입력한 데이터 가져오기
            lecture_name = form.cleaned_data.get('lecture_name')
            chapter_name = form.cleaned_data.get('chapter_name')

            # 현재 사용자의 lecture_name이 이미 존재하는지 확인
            existing_lecture = LectureChapter.objects.filter(user=request.user, lecture__title=lecture_name).first()

            if existing_lecture:
                # 해당 lecture_name이 이미 존재하는 경우
                # lecture_name에 하위 목록 추가
                LectureChapter.objects.create(user=request.user, lecture=existing_lecture.lecture, chapter_name=chapter_name)
                print("기존 강의에 챕터를 추가하였습니다.")
            else:
                # 해당 lecture_name이 존재하지 않는 경우
                # 새로운 강의 및 챕터 추가
                lecture = Lecture.objects.create(title=lecture_name)
                LectureChapter.objects.create(user=request.user, lecture=lecture, chapter_name=chapter_name)
                print("새로운 강의 및 챕터를 추가하였습니다.")

            messages.success(request, '강의 챕터가 성공적으로 추가되었습니다.')
            return render(request, "user/add_lecture_chapter.html")
    else:
        form = LectureChapterForm()

    # 폼 유효성 검사 실패 시에도 폼과 함께 에러 메시지를 전달
    if form.errors:
        # 폼에서 입력한 데이터 가져오기
        lecture_name = form.cleaned_data.get('lecture_name')
        chapter_name = form.cleaned_data.get('chapter_name')
        
        # 터미널에 출력
        print("User:", request.user)
        print("Lecture:", lecture_name)
        print("Chapter Name:", chapter_name)
        print("강의 챕터 추가에 실패했습니다.")

        messages.error(request, '강의 챕터 추가에 실패했습니다. 입력을 다시 확인해주세요.')
        print("강의 챕터 추가에 실패했습니다.")

    return render(request, 'user/add_lecture_chapter.html')




def lecture_detail_view(request, lecture_title):
    # lecture_title에 해당하는 LectureChapter 객체 가져오기
    lecture_chapters = LectureChapter.objects.filter(lecture__title=lecture_title)
    return render(request, 'lecture_detail.html', {'lecture_title': lecture_title, 'lecture_chapters': lecture_chapters})

def chapter_detail_view(request, lecture_title, chapter_name):
    # lecture_title과 chapter_name에 해당하는 LectureChapter 객체 가져오기
    lecture_chapter = LectureChapter.objects.filter(lecture__title=lecture_title, chapter_name=chapter_name).first()
    return render(request, 'chapter_detail.html', {'lecture_chapter': lecture_chapter})


