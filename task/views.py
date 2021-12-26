from django.contrib.auth import models
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from . models import Task
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='login')
def home(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'base.html', {'tasks': tasks})


def add_todo(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    if request.method == "POST":
        task = request.POST['task']

        task = Task.objects.create(
            task=task,
            user=request.user
        )
        task.save()
    return render(request, 'components/tasks.html', {'tasks': tasks})


def delete_todo(request, id):
    todo = Task.objects.get(pk=id)
    print(todo)
    todo.delete()
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'components/tasks.html', {'tasks': tasks})


def mark_complete(request, id):
    task = Task.objects.get(pk=id)
    print(task)
    if request.method == "POST":
        if task.task_status == False:
            task.task_status = True
        else:
            task.task_status = False
    task.save()
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'components/tasks.html', {'tasks': tasks})


def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username'].lower()
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already exists')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.warning(request, 'Email already registered')
                    return redirect('register')

                else:
                    user = User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        username=username,
                        email=email,
                        password=password,
                    )

                    # user.is_active = False
                    user.save()
                    return redirect('login')
        else:
            messages.warning(request, "Password don't Match")
            return redirect('register')

    return render(request, 'components/register.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login Success")
            return redirect('home')
        else:
            messages.warning(request, "Invalid Credentials")
            return redirect('login')

    return render(request, 'components/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "You have been successfully logged out")
    return redirect('login')


def check_user(request):
    if request.method == "POST":
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            return HttpResponse('<span id = "username-check" class="warning-text font-weight-bold lead small text-danger px-2">Username already exists.</span')
        else:
            return HttpResponse('<span id = "username-check" class="warning-text lead small font-weight-bold text-danger px-2">Username available.</span')


def email_check(request):
    if request.method == "POST":
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            return HttpResponse('<span id = "email-check" class="warning-text font-weight-bold lead small text-danger px-2">Email already exists.</span')
        else:
            return HttpResponse('<span id = "email-check" class="warning-text font-weight-bold lead small text-danger px-2">Email Not registered</span')
