from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm


def login_user(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You were logged in!!"))
            return redirect("home")
        else:
            messages.success(request, ("Username or Password is INCORRECT. Please Try Again!!!!"))
            return redirect("login")
    return render(request, "authenticate/login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out!!"))
    return redirect("login")


def register_user(request):
    if request.method=="POST":
        form=RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password1"]
            user=authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("Registeration Successful !!!"))
            return redirect("home")
    else:
        form=RegisterUserForm()
    return render(request, "authenticate/register_user.html", {"form": form})