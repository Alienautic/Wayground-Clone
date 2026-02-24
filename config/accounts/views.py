from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, "profile.html", {
        "profile": profile
    })

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(username=username, password=password)

        Profile.objects.create(
            user=user,
            role=role
        )

        login(request, user)
        return redirect("dashboard")

    return render(request, "register.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")

    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect("login")