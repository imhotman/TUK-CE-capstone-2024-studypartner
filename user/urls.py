from django.urls import path
from .views import lecture_list_view
from . import views

app_name = "user"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path('lecture_list/', views.lecture_list_view, name='lecture_list'),
    path('add_lecture_chapter/', views.add_lecture_chapter, name='add_lecture_chapter'),
]