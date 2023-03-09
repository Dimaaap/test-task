import csv
from datetime import datetime
from random import randint
import os

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from faker import Faker

from .forms import FakeCSVSchemaForm, CreateField, CountFields
from .models import FakeCVSSchema, CVSSchemaFields
from .services import *


@login_required(login_url='user_login')
def create_new_schema(request):
    if request.method == 'POST':
        form = FakeCSVSchemaForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            delimiter_char = form.cleaned_data['delimiter']
            new_schema = FakeCVSSchema(author=request.user, title=title,
                                       delimiter=delimiter_char)
            try:
                new_schema.save()
                return redirect('schemas_list')
            except (Exception,) as e:
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
    count_fields = filter_fields_in_db(CVSSchemaFields, 'schema', schema.id).count()
    if not schema:
        return redirect('main_page')
    if request.method == 'POST':
        form = CountFields(request.POST)
        if int(form['count_field'].value()) > count_fields:
            messages.error(request, 'Кількість полів перевищує ту кількість,яка у вас задана')
        else:
            request.session['count_field'] = int(form['count_field'].value())
    else:
        form = CountFields()
        form.fields['count_field'].initial = count_fields
    fields = filter_fields_in_db(CVSSchemaFields, 'schema', schema)
    return render(request, 'data/schema_page.html', {'schema': schema, 'fields': fields, 'form': form})


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
    except (Exception,):
        return HttpResponse('Помилка')
    return redirect('schema_page', schema.pk)


def form_csv(request, pk):
    fake = Faker()
    choice_dict = settings.FIELDS_DICT
    data_schema = get_field_from_db(FakeCVSSchema, 'id', pk)
    schema_fields = filter_fields_in_db(CVSSchemaFields, 'schema', data_schema.pk)
    filename = data_schema.title + str(randint(1, 10)) + '.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    with open(filename, 'w', encoding='utf-8-sig') as f:
        # writer = csv.writer(f, delimiter=data_schema.delimiter)
        writer = csv.writer(response)
        header = [column.name for column in schema_fields]
        writer.writerow(header)
        count_fields = schema_fields.count()
        for i in range(request.session['count_field']):
            row = []
            for column in schema_fields.all():
                if column.field == 'Число':
                    min_value = column.range_min if column.range_min else 0
                    max_value = column.range_max if column.range_max else 100
                    row.append(randint(min_value, max_value))
                elif column.field == 'Текст':
                    min_value = column.range_min if column.range_min else 1
                    max_value = column.range_max if column.range_max else 10
                    row.append(fake.text(randint(min_value + 5, max_value + 5)))
                else:
                    row.append(choice_dict[column.field])
            writer.writerow(row)
    # return HttpResponse(filename)
    return response
