from django.urls import path

from .views import *


urlpatterns = [
    path('', create_new_schema, name='main_form_page'),
    path('list', schemas_list, name='schemas_list')
]