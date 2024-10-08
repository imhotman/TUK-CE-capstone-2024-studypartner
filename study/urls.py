"""
URL configuration for study project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('signup_done/', views.signup_done, name='signup_done'),
    path('mypage/', views.mypage, name='mypage'),
    path('notice/', views.notice, name='notice'),
    path('qna/', views.qna, name='qna'),
    # path('lecture', views.lecture, name='lecture'),
    path('chapter/', views.chapter, name='chapter'),
    path('user/', include('user.urls')),
    path('upload/', include('upload.urls')),
    path('summary/', include('summary.urls')),
    path('chatting/', include('chatting.urls')),
    path('delete_done/', views.delete_done, name='delete_done'),

    path('delete_record/<int:record_id>/', views.delete_record_view, name='delete_record'),
    path('delete_studyrecord/<int:record_id>/', views.delete_studyrecord_view, name='delete_studyrecord'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static (
                    settings.MEDIA_URL,
                    document_root=settings.MEDIA_ROOT
)