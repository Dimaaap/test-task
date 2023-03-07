from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import FakeCSVSchemaForm, CreateField
from .models import FakeCVSSchema, CVSSchemaFields
from .services import *


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


def schema_page(request, pk):
    try:
        schema = FakeCVSSchema.objects.get(id=pk)
    except Exception:
        return redirect('main_page')
    return render(request, 'data/schema_page.html', {'schema': schema})


def delete_schema(request, pk):
    try:
        FakeCVSSchema.objects.filter(pk=pk).delete()
    except Exception:
        print('dsadsa')
    return redirect(schemas_list)


def add_field(request, pk):
    schema = FakeCVSSchema.objects.get(pk=pk, author=request.user)
    if request.method == 'POST':
        form = CreateField(request.POST)
        new_field = form.save(commit=False)
        new_field.schema = schema
        new_field.save()
        messages.success(request, 'Поле успішно додано')
        return redirect(schema_page, pk)
    else:
        form = CreateField()
    return render(request, 'data/add_field.html', {'form': form})
