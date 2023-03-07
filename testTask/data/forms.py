from django import forms
from django.contrib.auth import get_user_model

from .models import FakeCVSSchema, CVSSchemaFields

user_model = get_user_model()


class FakeCSVSchemaForm(forms.Form):
    title = forms.CharField(label="Введіть ім'я схеми", required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))


class CreateField(forms.ModelForm):
    class Meta:
        model = CVSSchemaFields
        # fields = '__all__'
        exclude = ('schema',)

    name = forms.CharField(label='Введіть назву поля',
                           required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    order = forms.IntegerField(label='Виберіть порядок поля', required=False)
    range_min = forms.IntegerField(label='Оберіть мінімальне значення', required=False)
    range_max = forms.IntegerField(label='Оберіть максимальне значення', required=False)
