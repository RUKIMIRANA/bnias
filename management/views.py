from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as login_me_in, logout as log_me_out


# Create your views here.
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "GET":
        return render(request, "auth/register.html")

    elif request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == "" or password != confirm_password:
            messages.info(request, "Password do not match")
            return redirect("register")

        if email == "" or User.objects.filter(email=email).exists():
            messages.info(request, "Email already taken")
            return redirect("register")

        if username == "" or User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect("register")

        new_user = User.objects.create_user(
            username=username, email=email, password=password
        )
        new_user.save()

        user_login = authenticate(username=username, password=password)
        login_me_in(request, user_login)

        return redirect("home")


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "GET":
        return render(request, "auth/login.html")

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is None:
            messages.info(request, "Invalid credentials")
            return redirect("login")

        login_me_in(request, user)
        return redirect("home")


@login_required(login_url="login")
def logout(request):
    log_me_out(request)
    return redirect("home")
