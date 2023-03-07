from django import forms
from django.forms import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

user_form = get_user_model()


class UserLoginForm(forms.Form):

    class Meta:
        model = user_form
        fields = ('username', 'password1')

    username = forms.CharField(label='Ваш логін',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Ваш пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user_form.objects.get(username=username)
        except Exception:
            raise ValidationError('Неправильний логін або пароль')
        return username

