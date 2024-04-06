from django.urls import path
from . import views

app_name = "summary"

urlpatterns = [
    # chapter에 대한 URL 패턴
    path('summary_detail/<str:lecture_name>/<str:chapter_name>/', views.summary_detail_view, name='summary_detail'),  # summary_detail
    path('upload_file_summary/<str:lecture_name>/<str:chapter_name>/', views.upload_file_summary, name='upload_file_summary'),
]

