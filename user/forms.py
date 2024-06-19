from django import forms
from .models import LectureChapter, UploadFile_handwriting

class LectureChapterForm(forms.ModelForm):
    lecture_name = forms.CharField(max_length=100, label='강의')
    
    class Meta:
        model = LectureChapter
        fields = ['lecture_name', 'chapter_name']  # 사용자에게 입력받을 필드 지정


class UploadFile_handwritingForm(forms.ModelForm):
    class Meta:
        model = UploadFile_handwriting
        fields = ['file_title', 'file_name']    # 사용자에게 입력받을 필드 지정