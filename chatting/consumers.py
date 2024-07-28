# # consumers.py

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer # type: ignore
# from django.contrib.auth.models import User
# from .models import PrivateChatRoom, PrivateMessage

# class ChatConsumer(AsyncWebsocketConsumer):
#     # 클라이언트가 WebSocket 연결을 요청했을 때 호출됩니다.
#     async def connect(self):
#         # 현재 사용자와 대화 상대 사용자 ID를 가져옵니다.
#         self.user = self.scope['user']
#         print(self.user)
#         self.other_user_id = self.scope['url_route']['kwargs']['room_name']
#         self.other_user = await self.get_user(self.other_user_id)
        
#         # 사용자가 인증되지 않았거나 대화 상대가 유효하지 않은 경우 연결을 닫습니다.
#         if not self.user.is_authenticated or not self.other_user:
#             print("사용자가 인증되지 않았습니다.")
#             await self.close()

#         # 채팅방 그룹 이름을 설정합니다. 사용자 ID를 기준으로 그룹 이름을 생성합니다.
#         self.room_group_name = f'chat_{min(self.user.id, self.other_user.id)}_{max(self.user.id, self.other_user.id)}'

#         # 채널 레이어에 그룹을 추가합니다.
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         # WebSocket 연결을 수락합니다.
#         await self.accept()

#     # 클라이언트가 연결을 끊었을 때 호출됩니다.
#     async def disconnect(self, close_code):
#         # 채널 레이어에서 그룹을 제거합니다.
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # 클라이언트가 메시지를 보냈을 때 호출됩니다.
#     async def receive(self, text_data):
#         # 수신된 텍스트 데이터를 JSON 형식으로 파싱합니다.
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # 새 메시지를 데이터베이스에 저장합니다.
#         private_message = await self.create_message(message)

#         # 채널 레이어를 통해 그룹에 메시지를 전송합니다.
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'user': self.user.username,
#                 'message_id': private_message.id,
#                 'is_read': private_message.is_read,
#             }
#         )

#     # 채널 레이어를 통해 그룹에 전송된 메시지를 수신합니다.
#     async def chat_message(self, event):
#         message = event['message']
#         user = event['user']
#         message_id = event['message_id']
#         is_read = event['is_read']

#         # 클라이언트에게 메시지를 JSON 형식으로 전송합니다.
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'user': user,
#             'message_id': message_id,
#             'is_read': is_read,
#         }))

#     # 새 메시지를 데이터베이스에 저장합니다.
#     async def create_message(self, message):
#         # 현재 사용자와 대화 상대를 기준으로 채팅방을 생성합니다.
#         chat_room, created = await PrivateChatRoom.objects.get_or_create(
#             user1=self.user if self.user.id < self.other_user.id else self.other_user,
#             user2=self.other_user if self.user.id < self.other_user.id else self.user
#         )
#         # 새로운 메시지를 데이터베이스에 저장합니다.
#         private_message = await PrivateMessage.objects.create(
#             chat_room=chat_room,
#             sender=self.user,
#             receiver=self.other_user,
#             content=message
#         )
#         return private_message

#     # 사용자 ID로 사용자 객체를 비동기적으로 가져옵니다.
#     @staticmethod
#     async def get_user(user_id):
#         try:
#             return await User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return None



# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async
# from django.contrib.auth.models import User
# from .models import PrivateChatRoom, PrivateMessage

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope['user']
#         self.other_user_id = self.scope['url_route']['kwargs']['room_name']

#         # Debug: Check the values of self.user and self.other_user_id
#         print(f"Connecting user: {self.user}, other_user_id: {self.other_user_id}")

#         self.other_user = await self.get_user(self.other_user_id)

#         # Debug: Check if self.other_user is None
#         if self.other_user is None:
#             print(f"User with id {self.other_user_id} does not exist.")
        
#         if not self.user.is_authenticated or not self.other_user:
#             await self.close()
#             return

#         self.room_group_name = f'chat_{min(self.user.id, self.other_user.id)}_{max(self.user.id, self.other_user.id)}'

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         private_message = await self.create_message(message)

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'user': self.user.username,
#                 'message_id': private_message.id,
#                 'is_read': private_message.is_read,
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']
#         user = event['user']
#         message_id = event['message_id']
#         is_read = event['is_read']

#         await self.send(text_data=json.dumps({
#             'message': message,
#             'user': user,
#             'message_id': message_id,
#             'is_read': is_read,
#         }))

#     @sync_to_async
#     def create_message(self, message):
#         chat_room, created = PrivateChatRoom.objects.get_or_create(
#             user1=self.user if self.user.id < self.other_user.id else self.other_user,
#             user2=self.other_user if self.user.id < self.other_user.id else self.user
#         )
#         private_message = PrivateMessage.objects.create(
#             chat_room=chat_room,
#             sender=self.user,
#             receiver=self.other_user,
#             content=message
#         )
#         return private_message

#     @sync_to_async
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return None



# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async
# from django.contrib.auth.models import User
# from .models import PrivateChatRoom, PrivateMessage

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope['user']
#         self.other_user_id = self.scope['url_route']['kwargs']['room_name']
        
#         # Debug: Check the values of self.user and self.other_user_id
#         print(f"Connecting user: {self.user}, other_user_id: {self.other_user_id}")

#         self.other_user = await self.get_user(self.other_user_id)

#         # Debug: Check if self.other_user is None
#         if self.other_user is None:
#             print(f"User with id {self.other_user_id} does not exist.")
        
#         if not self.user.is_authenticated or not self.other_user:
#             await self.close()
#             return

#         self.room_group_name = f'chat_{min(self.user.id, self.other_user.id)}_{max(self.user.id, self.other_user.id)}'

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         private_message = await self.create_message(message)

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'user': self.user.username,
#                 'message_id': private_message.id,
#                 'is_read': private_message.is_read,
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']
#         user = event['user']
#         message_id = event['message_id']
#         is_read = event['is_read']

#         print(f"Sending message to frontend: {message} from user: {user}") # 확인용 로그

#         await self.send(text_data=json.dumps({
#             'message': message,
#             'user': user,
#             'message_id': message_id,
#             'is_read': is_read,
#         }))

#     @sync_to_async
#     def create_message(self, message):
#         chat_room, created = PrivateChatRoom.objects.get_or_create(
#             user1=self.user if self.user.id < self.other_user.id else self.other_user,
#             user2=self.other_user if self.user.id < self.other_user.id else self.user
#         )
#         private_message = PrivateMessage.objects.create(
#             chat_room=chat_room,
#             sender=self.user,
#             receiver=self.other_user,
#             content=message
#         )
#         return private_message

#     @sync_to_async
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return None



import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import PrivateChatRoom, PrivateMessage
from .views import get_or_create_chat_room

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.other_user_id = self.scope['url_route']['kwargs']['room_name']
        self.other_user = await self.get_user(self.other_user_id)

        if not self.user.is_authenticated or not self.other_user:
            await self.close()

        self.room_group_name = f'chat_{min(self.user.id, self.other_user.id)}_{max(self.user.id, self.other_user.id)}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print("연결여부: 연결됨.")

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("연결여부: 연결 해제됨.")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        print(f"Received message from client: {message}")

        private_message = await self.create_message(message)
        print(f"Message created in DB: {private_message.content}")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'message_id': private_message.id,
                'is_read': private_message.is_read,
            }
        )
        print(f"Message sent to group: {self.room_group_name}")

    async def chat_message(self, event):
        print(f"chat_message handler called with event: {event}")  # 추가 로그

        message = event['message']
        user = event['user']
        message_id = event['message_id']
        is_read = event['is_read']

        print(f"Sending message to frontend: {message} from user: {user}")

        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'message_id': message_id,
            'is_read': is_read,
        }))
        print("Message sent to frontend")

    @sync_to_async
    def create_message(self, message):
        chat_room, created = get_or_create_chat_room(self.user, self.other_user)
        private_message = PrivateMessage.objects.create(
            chat_room=chat_room,
            sender=self.user,
            receiver=self.other_user,
            content=message
        )
        return private_message

    @sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None




