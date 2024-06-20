from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path('lecture_list/', views.lecture_list_view, name='lecture_list'),
    path('lecture/', views.lecture_view, name='lecture'),
    path('add_lecture_chapter/', views.add_lecture_chapter_view, name='add_lecture_chapter'),
    path('timer/', views.timer_view, name='timer'),
    path('friend_record/', views.friend_record_view, name='friend_record'),
    path('today_records/', views.today_records_view, name='today_records'),
    
    path('handwriting/<str:lecture_name>/<str:chapter_name>/', views.handwriting_view, name='handwriting'),

    path('upload_file_handwriting/<str:lecture_name>/<str:chapter_name>/', views.upload_file_handwriting, name='upload_file_handwriting'),
    path('delete_file_handwriting/<int:file_id>/', views.delete_file_handwriting, name='delete_file_handwriting'),
    
    path('timer_test1/', views.timer_test1_view, name='timer_test1'),
    path('update-session/', views.update_session_view, name='update_session'),
    path('add_timer/', views.add_timer_view, name='add_timer'),
    path('lecture_sidebar/', views.lecture_sidebar_view, name='lecture_sidebar'),
    path('delete_account/', views.delete_account_view, name='delete_account'),
    path('lecture/<int:lecture_id>/delete_chapter/<int:chapter_id>/', views.delete_chapter, name='delete_chapter'),
    path('friend/', views.friend_view, name='friend'),
    path('send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('delete_friend/<int:friend_id>/', views.delete_friend, name='delete_friend'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),



  

    # lecture에 대한 URL 패턴
    path('lecture_detail/<str:lecture_name>/', views.lecture_detail_view, name='lecture_detail'),  # lecture_detail_view
    # chapter에 대한 URL 패턴
    # path('chapter_detail/<str:lecture_name>/<str:chapter_name>/', views.chapter_detail_view, name='chapter_detail'),  # chapter_detail_view  
]
