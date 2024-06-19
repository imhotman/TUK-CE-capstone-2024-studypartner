from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from user.models import Lecture, LectureChapter, Friendship, FriendRequest
from .models import UploadFile_summary
from .forms import UploadFile_summaryForm  # UploadFileForm을 가져옴
from django.urls import reverse
from django.http import Http404
import speech_recognition as sr
import wave
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os



# Create your views here.


# def summary_detail_view(request, lecture_name, chapter_name):
#     # 강의명과 챕터명이 일치하는 LectureChapter 객체를 가져옴
#     chapter = LectureChapter.objects.filter(lecture__title=lecture_name, chapter_name=chapter_name).first()

#     # 현재 로그인한 사용자 정보를 가져옴
#     current_user = request.user

#     # LectureChapter가 없는 경우 404 에러 반환
#     if not chapter:
#         raise Http404("챕터를 찾을 수 없습니다.")

#     # 해당 챕터에 업로드된 파일들 가져오기
#     uploaded_files = UploadFile_summary.objects.filter(chapter=chapter)

#     # 파일 업로드를 위한 폼 생성
#     form = UploadFile_summaryForm(request.POST or None, request.FILES or None)

#     context = {
#         'chapter': chapter,
#         'uploaded_files': uploaded_files,  # 업로드된 파일들을 context에 추가
#         'form': form,  # 폼을 context에 추가
#     }

#     return render(request, "summary/summary_detail.html", context)



def summary_detail_view(request, lecture_name, chapter_name):
    # 강의명과 챕터명이 일치하는 LectureChapter 객체를 가져옴
    chapter = LectureChapter.objects.filter(lecture__title=lecture_name, chapter_name=chapter_name).first()

    # 현재 로그인한 사용자 정보를 가져옴
    current_user = request.user
    lecture_chapters = LectureChapter.objects.filter(user=current_user).select_related('lecture').order_by('lecture__title')

    # LectureChapter가 없는 경우 404 에러 반환
    if not chapter:
        raise Http404("챕터를 찾을 수 없습니다.")

    lectures = []
    for chapter_obj in lecture_chapters:
        lecture_title = chapter_obj.lecture.title
        chapter_name = chapter_obj.chapter_name
        lecture_url = reverse('user:lecture_detail', kwargs={'lecture_name': lecture_title})
        chapter_url = reverse('upload:chapter_detail', kwargs={'lecture_name': lecture_title, 'chapter_name': chapter_name})

        # 현재 강의가 lectures 리스트에 없으면 추가
        if not any(lecture['lecture'] == lecture_title for lecture in lectures):
            lectures.append({'lecture': lecture_title, 'chapters': []})

        # 현재 챕터 추가
        lectures[-1]['chapters'].append({'chapter_name': chapter_name, 'chapter_url': chapter_url, 'lecture_url': lecture_url})

    # 해당 챕터에 업로드된 파일들 가져오기
    uploaded_files = UploadFile_summary.objects.filter(chapter=chapter)

    # 파일 업로드를 위한 폼 생성
    form = UploadFile_summaryForm(request.POST or None, request.FILES or None)    

    # 현재 사용자의 친구 요청 가져오기
    friend_requests = FriendRequest.objects.filter(to_user=request.user)

    # 현재 사용자의 친구 목록 가져오기
    user = request.user
    friends = Friendship.objects.filter(user=user).select_related('friend')

    context = {
        'chapter': chapter,
        'lectures': lectures,
        'chapter_name': chapter_name,
        'uploaded_files': uploaded_files,  # 업로드된 파일들을 context에 추가
        'form': form,  # 폼을 context에 추가
        'request_user': user,
        'friend_requests': friend_requests,
        'friends': friends,
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


def delete_file_summary(request, file_id):
    file_to_delete = get_object_or_404(UploadFile_summary, id=file_id)
    lecture_name = file_to_delete.chapter.lecture.title
    chapter_name = file_to_delete.chapter.chapter_name
    file_to_delete.delete()
    return redirect('summary:summary_detail', lecture_name=lecture_name, chapter_name=chapter_name)








# STT 함수
def stt(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio, language='ko')
        return text
    except sr.UnknownValueError:
        return '인식 실패'
    except sr.RequestError as e:
        return f"요청 실패: {e}"

# AI 요약하기를 처리할 view 함수
def stt_view(request, file_id):
    audio_file = get_object_or_404(UploadFile_summary, pk=file_id)
    text = stt(audio_file.file_name.path)
    
    context = {
        'text': text,
        'audio_file': audio_file
    }

    return render(request, 'summary/show_stt.html', context)















def generate_response(sys_message, user_message):
    os.environ['HF_TOKEN'] = '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'

    model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

    # 파인 튜닝
    #pipeline = transformers.pipeline(
    #    "text-generation",
    #    model=model_id,
    #    model_kwargs={"torch_dtype": torch.bfloat16}, 
    #    device_map="auto",
    #)

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype = torch.bfloat16,
        device_map = "auto",
    )

    messages = [
        {"role": "system", "content": f"{sys_message}"},
        {"role": "user", "content": f"{user_message}"},
    ]

    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = model.generate(
        input_ids,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
    )
    response = outputs[0][input_ids.shape[-1]:]

    return tokenizer.decode(response, skip_special_tokens = True)



sys_message = '너는 요약을 수행하는 챗봇이야. 핵심 내용만 256토큰 이내로 한국어로 요약해줘'
ori_txt = """'다음과 같다. 하의도에 상륙한 신한공사 사원과 경관 등은 소작료를 강제 징수하기 위해 2개조로 나뉘어, 제1대는 오림리, 제2대는 대리로 향했다.
            오림리에 도착한 제1대는 곧바로 가택 수색을 하고, 노인과 부녀자들에게까지 ‘소작료를 내지 않으면 총살시키겠다’고 위협하면서 농민들을 폭행했다.
            농민 200여명이 경관의 행위에 항의하자, 경관대는 실탄을 장전해 농민에게 무차별 사격을 가했는데 그 과정에서 朴鍾彩가 중상을 입었다.'"""

if __name__ == "__main__":
    summary_text = generate_response(sys_message, ori_txt)
    print(summary_text)