from django.urls import path
from . import views

app_name = "upload"

urlpatterns = [
    # chapter에 대한 URL 패턴
    path('chapter_detail/<str:lecture_name>/<str:chapter_name>/', views.chapter_detail_view, name='chapter_detail'),  # chapter_detail_view
    path('upload_file/<str:lecture_name>/<str:chapter_name>/', views.upload_file, name='upload_file'),
]

