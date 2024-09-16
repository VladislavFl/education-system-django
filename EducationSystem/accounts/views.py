from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import user_in_group

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            student_group = Group.objects.get(name='Student')
            user.groups.add(student_group)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home') # Перенаправление в личный кабинет
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    messages.error(request, 'Учетная запись неактивна.')
            else:
                messages.error(request, 'Неправильное имя пользователя или пароль.')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def teacher_profile(request):
    return render(request, 'accounts/teacher_profile.html', {'user': request.user})

@login_required
def student_profile(request):
    return render(request, 'accounts/student_profile.html', {'user': request.user})

@login_required
def profile(request):
    if user_in_group(request.user, 'Teacher'):
        return render(request, 'accounts/teacher_profile.html', {'user': request.user})
    elif user_in_group(request.user, 'Student'):
        return render(request, 'accounts/student_profile.html', {'user': request.user})
