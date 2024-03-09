from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(username=username, password=password)

        if user is not None:
            print("인증성공")
            messages.success(request, "로그인 성공!")
            login(request, user)
        else:
            messages.error(request, "인증 실패")
            print("인증실패")

    return render(request, "user/login.html")

def logout_view(request):
    logout(request)
    print("로그아웃")
    return redirect("user:login")

def signup_view(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "회원가입 성공!")
        print("회원가입 성공")
        return redirect("user:login")

    return render(request, "user/signup.html")