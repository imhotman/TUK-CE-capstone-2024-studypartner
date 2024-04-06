from django.contrib.auth.models import User
from django.db import models
from user.models import Lecture, LectureChapter

class UploadFile_summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # lecture = models.ForeignKey(LectureChapter, related_name='uploaded_files', on_delete=models.CASCADE, null=True)
    chapter = models.ForeignKey(LectureChapter, on_delete=models.CASCADE, null=True)
    file_title = models.CharField(max_length=50, default="")
    file_name = models.FileField(null=True)

    def __str__(self):

        # return f"사용자={self.user}, 강의명={self.lecture}, 챕터명={self.chapter}, 파일 제목={self.file_title}, 파일 이름={self.file_name}"
        return f"사용자: {self.user}, 강의&챕터명: {self.chapter}, 파일 제목: {self.file_title}, 파일 이름: {self.file_name}"    