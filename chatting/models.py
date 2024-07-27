from django.contrib.auth.models import User
from django.db import models
from user.models import Lecture, LectureChapter, Study_TimerSession, FriendRequest, Friendship, UploadFile_handwriting
from django.db.models import UniqueConstraint
from summary.models import UploadFile_summary


# 개인 채팅방 모델 정의
class PrivateChatRoom(models.Model):
    # 채팅방 사용자 1을 나타내는 외래 키 필드
    user1 = models.ForeignKey(User, related_name='chat_user1', on_delete=models.CASCADE)
    # 채팅방 사용자 2를 나타내는 외래 키 필드
    user2 = models.ForeignKey(User, related_name='chat_user2', on_delete=models.CASCADE)

    def __str__(self):
        # 문자열 표현: 두 사용자의 사용자 이름을 표시합니다.
        return f'대화상대1: {self.user1.username}, 대화상대2: {self.user2.username}'


# 개인 메시지 모델 정의
class PrivateMessage(models.Model):
    # 메시지가 속한 채팅방
    chat_room = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE)
    # 메시지를 보낸 사용자
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    # 메시지를 받는 사용자
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
     # 메시지의 내용을 저장하는 필드, 빈 값 허용
    content = models.TextField(blank=True, null=True)
    # 메시지에 첨부된 파일, 빈 값 허용
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
     # 메시지가 생성된 시간을 자동으로 저장하는 필드
    timestamp = models.DateTimeField(auto_now_add=True)
    # 메시지가 읽혔는지 여부를 나타내는 필드, 기본값 = False
    is_read = models.BooleanField(default=False)

    def __str__(self):
        # 문자열 표현: 발신자와 메시지 내용을 표시합니다.
        return f'보낸사람: {self.sender.username}, 대화내용: {self.content or "파일 업로드"}'

    class Meta:
        # 메타 데이터: 특정 필드 조합의 유일성을 보장합니다.
        constraints = [
            models.UniqueConstraint(
                fields=['sender', 'receiver', 'timestamp'],  # 유일성을 보장할 필드 조합
                name='unique_message'  # 제약 조건 이름
            )
        ]
   