from django import forms
from .models import UploadFile_summary

class UploadFile_summaryForm(forms.ModelForm):
    class Meta:
        model = UploadFile_summary
        fields = ['file_title', 'file_name']    # 사용자에게 입력받을 필드 지정
