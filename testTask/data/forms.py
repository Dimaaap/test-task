from django import forms
from django.contrib.auth import get_user_model

from .models import FakeCVSSchema

user_model = get_user_model()


class FakeCSVSchemaForm(forms.Form):
    title = forms.CharField(label="Введіть ім'я схеми", required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))

