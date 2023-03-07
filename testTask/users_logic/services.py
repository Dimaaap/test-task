from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .forms import UserLoginForm


def user_authenticate(request, form: UserLoginForm):
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    new_user = authenticate(username=username, password=password)
    if new_user:
        login(request, new_user)
        messages.success(request, 'Ви авторизувались на сайті')
    else:
        messages.error(request, 'Неправильний логін або пароль')


def redirect_user_login(view_func, redirect_url='main_page'):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(redirect_url, permanent=True)
        else:
            return view_func(request, *args, **kwargs)
    return wrapper
