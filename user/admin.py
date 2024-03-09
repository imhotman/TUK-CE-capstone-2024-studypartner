from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'email')

admin.site.register(User, UserAdmin) # User 모델을 등록합니다.