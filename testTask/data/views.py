import csv
from datetime import datetime
from random import randint
import io

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from faker import Faker


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
                return redirect('schemas_list')
            except (Exception, ) as e:
                print(e)
                messages.error(request, 'Помилка створення схеми')
        else:
            messages.error(request, 'Помилка додавання схеми')
            print(form.errors)
    else:
        form = FakeCSVSchemaForm()
    return render(request, 'data/create_schema_form.html', {'form': form})


def schemas_list(request):
    query = filter_fields_in_db(FakeCVSSchema, 'author', request.user)
    return render(request, 'data/schemas_list.html', {'query': query})


def schema_page(request, pk):
    schema = get_field_from_db(FakeCVSSchema, 'id', pk)
    if not schema:
        return redirect('main_page')
    fields = filter_fields_in_db(CVSSchemaFields, 'schema', schema)
    return render(request, 'data/schema_page.html', {'schema': schema, 'fields': fields})


def delete_schema(request, pk):
    delete_data_from_db(FakeCVSSchema, 'pk', pk)
    return redirect(schemas_list)


def add_field(request, pk):
    schema = FakeCVSSchema.objects.get(pk=pk, author=request.user)
    if request.method == 'POST':
        form = CreateField(request.POST)
        if form.is_valid():
            new_field = form.save(commit=False)
            new_field.schema = schema
            new_field.save()
            return redirect(schema_page, pk)
    else:
        form = CreateField()
    return render(request, 'data/add_field.html', {'form': form})


def delete_field(request, pk):
    field = get_field_from_db(CVSSchemaFields, 'pk', pk)
    if not field:
        return HttpResponse('Помилка')
    schema = get_field_from_db(FakeCVSSchema, 'pk', field.schema.pk)
    try:
        field.delete()
    except (Exception, ):
        return HttpResponse('Помилка')
    return redirect('schema_page', schema.pk)


def form_csv(request, pk):
    faker = Faker()



