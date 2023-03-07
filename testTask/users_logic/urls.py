from django.urls import path, include

from .views import *


urlpatterns = [
    path('', main_page_view, name='main_page'),
    #path('register', signup_view, name='user_register'),
    path('login', login_view, name='user_login'),
    path('logout', Logout.as_view(), name='user_logout')
]