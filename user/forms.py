from django import forms
from .models import LectureChapter

class LectureChapterForm(forms.ModelForm):
    lecture_name = forms.CharField(max_length=100, label='강의')
    
    class Meta:
        model = LectureChapter
        fields = ['lecture_name', 'chapter_name']  # 사용자에게 입력받을 필드 지정