from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserLoginForm
from .services import user_authenticate, redirect_user_login


def main_page_view(request):
    return render(request, template_name='users_logic/main_page.html')


@redirect_user_login
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user_authenticate(request, form)
    else:
        form = UserLoginForm()
    return render(request, 'users_logic/user_login.html', {'form': form})


class Logout(generic.View, LoginRequiredMixin):
    login_url = reverse_lazy('user_register')

    def get(self, request):
        logout(request)
        return render(request, template_name='users_logic/user_logout.html')
