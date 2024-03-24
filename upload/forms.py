from django import forms
from .models import UploadFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ['file_title', 'file_name']    # 사용자에게 입력받을 필드 지정

