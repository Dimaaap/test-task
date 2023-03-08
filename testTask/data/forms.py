from django import forms
from django.contrib.auth import get_user_model

from .models import FakeCVSSchema, CVSSchemaFields

user_model = get_user_model()


class FakeCSVSchemaForm(forms.Form):
    POSSIBLE_DELIMITERS = (
        (',', 'Кома(,)'),
        (';', 'Крапка з комою(;)'),
        ('\t', 'Табуляція(\\t)'),
        (" ", "Пробіл(' ')"),
        ("|", "Вертикальна палочка('|')")
    )
    title = forms.CharField(label="Введіть ім'я схеми", required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    #delimiter = forms.CharField(label="Оберіть роздіюлювач для полів у CSV файлі",
    #                            widget=forms.Select(choices=POSSIBLE_DELIMITERS))

    def clean_title(self):
        title = self.cleaned_data['title']
        all_schemas = FakeCVSSchema.objects.filter(title=title)
        if all_schemas:
            raise forms.ValidationError('Схема з таким іменем вже існує')
        if len(title) > 20:
            raise forms.ValidationError('Назва схеми не повинна перевищувати 20 символів')
        return title



class CreateField(forms.ModelForm):
    class Meta:
        model = CVSSchemaFields
        exclude = ('schema',)

    name = forms.CharField(label='Введіть назву поля',
                           required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    order = forms.IntegerField(label='Виберіть порядок поля', required=False)
    range_min = forms.IntegerField(label='Оберіть мінімальне значення', required=False)
    range_max = forms.IntegerField(label='Оберіть максимальне значення', required=False)

    def clean_order(self):
        order = self.cleaned_data['order']
        if order and order < 0:
            raise forms.ValidationError('Порядок не може бути меншим нуля')

        return order

    def clean_range_min(self):
        range_min = self.cleaned_data['range_min']
        if range_min and (self.cleaned_data['field'] not in ('Число', 'Текст')):
            raise forms.ValidationError('Значення діапазону можна задавати лише для полів типу Текст'
                                        'або Число')
        return range_min
