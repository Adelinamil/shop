import logging

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from users.forms import UserRegisterForm, LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('shop:index')
            else:
                messages.error(request, "Неверный логин или пароль")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('users:login')


@require_POST
def check_user(request):
    column_name = request.POST.get('column_name', None)
    column_value = request.POST.get('column_value', None)
    try:
        return JsonResponse({'is_taken': User.objects.filter(**{column_name: column_value}).exists()})
    except Exception as e:
        logging.warning(e, exc_info=True)
        return JsonResponse(None)


@login_required
@require_POST
def confirm_password(request):
    password = request.POST.get('password', None)
    if authenticate(request, username=request.user.username, password=password):
        return JsonResponse({'is_correct': True})
    else:
        return JsonResponse({'is_correct': False})
