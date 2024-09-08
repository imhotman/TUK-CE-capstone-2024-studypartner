from django.urls import path
from . import views

app_name = "chatting"

urlpatterns = [
    path('chat/<int:user_id>/', views.private_chat_room, name='private_chat_room'),
    path('chatting_test/<int:user_id>/', views.chatting_test_view, name='chatting_test'),
    # path('delete_message/', views.delete_message, name='delete_message'),
]
