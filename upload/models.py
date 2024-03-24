from django.contrib.auth.models import User
from django.db import models
from user.models import Lecture, LectureChapter

class UploadFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    lecture = models.ForeignKey(Lecture, related_name='uploaded_files', on_delete=models.CASCADE, null=True)
    chapter = models.ForeignKey(LectureChapter, on_delete=models.CASCADE, null=True)
    file_title = models.CharField(max_length=50, default="")
    file_name = models.FileField(null=True)

    def __str__(self):
        lecture_title = self.lecture.title if self.lecture else 'No Lecture'
        chapter_name = self.chapter.chapter_name if self.chapter else 'No Chapter'
        return f"사용자={self.user}, 강의명={lecture_title}, 챕터명={chapter_name}, 파일 제목={self.file_title}, 파일 이름={self.file_name}"






# from django.contrib.auth.models import User
# from django.db import models
# from user.models import LectureChapter

# class UploadFile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # 현재 로그인한 사용자 정보를 저장하는 외래 키
#     lecture_chapter = models.ForeignKey(LectureChapter, on_delete=models.CASCADE)  # 챕터 정보를 저장하는 외래 키
#     file_title = models.CharField(default="", max_length=50)  # 파일 제목
#     file_name = models.FileField(null=True)  # 실제 파일

#     def __str__(self):
#         return f"사용자={self.user}, 강의&챕터명={self.lecture_chapter.chapter_name}, 파일 제목={self.file_title}, 파일 이름={self.file_name}"
