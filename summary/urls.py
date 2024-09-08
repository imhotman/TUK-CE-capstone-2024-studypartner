from django.urls import path, re_path
from . import views

app_name = "summary"

urlpatterns = [
    # chapter에 대한 URL 패턴
    path('summary_detail/<str:lecture_name>/<str:chapter_name>/', views.summary_detail_view, name='summary_detail'),  # summary_detail
    path('AI_summarypage/<str:lecture_name>/<str:chapter_name>/', views.AI_summarypage_view, name='AI_summarypage'),  # AI_summarypage

    path('upload_file_summary/<str:lecture_name>/<str:chapter_name>/', views.upload_file_summary, name='upload_file_summary'),
    path('delete_file_summary/<int:file_id>/', views.delete_file_summary, name='delete_file_summary'),
    path('stt_view/<str:lecture_name>/<str:chapter_name>/<int:file_id>/', views.stt_view, name='stt_view'),
    path('show_summary_view/<str:lecture_name>/<str:chapter_name>/<int:file_id>/', views.show_summary_view, name='show_summary_view'),
    path('get_file_size/<int:file_id>/', views.get_file_size, name='get_file_size'),
]

