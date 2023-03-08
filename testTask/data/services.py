from django.contrib import messages

from .models import FakeCVSSchema
from .filters import EqualFilter


def filter_fields_in_db(model: callable, field: str, value):
    custom_filter = EqualFilter()
    return model.objects.filter(**custom_filter(field, value))


def get_field_from_db(model: callable, field: str, value):
    equal_filter = EqualFilter()
    query = []
    try:
        query = model.objects.get(**equal_filter(field, value))
    except (Exception, ):
        query = []
    finally:
        return query


def delete_data_from_db(model: callable, field: str, value):
    filter_fields_in_db(model, field, value).delete()

