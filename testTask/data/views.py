from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import FakeCSVSchemaForm
from .models import FakeCVSSchema
from .services import *


# @login_required(login_url='user_login')
# def main_form_page_view(request):
#     if request.method == 'POST':
#         form = FakeCSVSchemaForm(request.POST)
#     else:
#         form = FakeCSVSchemaForm()
#     return render(request, 'data/main_data_form.html', {'form': form})


@login_required(login_url='user_login')
def create_new_schema(request):
    if request.method == 'POST':
        form = FakeCSVSchemaForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            new_schema = FakeCVSSchema(author=request.user, title=title)
            try:
                new_schema.save()
                messages.success(request, 'Схема успішно створена')
            except Exception:
                messages.error(request, 'Помилка створення схеми')
        else:
            messages.error(request, 'Помилка додавання схеми')
            print(form.errors)
    else:
        form = FakeCSVSchemaForm()
    return render(request, 'data/create_schema_form.html', {'form': form})


def schemas_list(request):
    query = FakeCVSSchema.objects.filter(author=request.user)
    return render(request, 'data/schemas_list.html', {'query': query})


def schema_page(request, schema_id):
    return render(request, 'data/schemas_list.html')
