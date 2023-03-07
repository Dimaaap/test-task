from django.urls import path

from .views import *


urlpatterns = [
    path('', create_new_schema, name='main_form_page'),
    path('list', schemas_list, name='schemas_list'),
    path('detail/<int:pk>/', schema_page, name='schema_page'),
    path('delete/<int:pk>/', delete_schema, name='delete_schema'),
    path('add/field/<int:pk>/', add_field, name='add_field')
]