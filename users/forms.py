import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def validate_first_name(value):
    if not re.match(r'^[а-яА-Я\-]+$', value):
        raise forms.ValidationError('Только кириллица, пробел и тире разрешены.')
    return value


def validate_last_name(value):
    if not re.match(r'^[а-яА-Я\-]+$', value):
        raise forms.ValidationError('Только кириллица, пробел и тире разрешены.')
    return value


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Почта')
    first_name = forms.CharField(
        max_length=100,
        label='Имя',
        validators=[validate_first_name],
        help_text='Не более 100 символов, кириллицей.',
        widget=forms.TextInput(
            attrs={
                'pattern': '[а-яА-Я\\-]+',
            }
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        label='Фамилия',
        validators=[validate_last_name],
        help_text='Не более 100 символов, кириллицей.',
        widget=forms.TextInput(
            attrs={
                'pattern': '[а-яА-Я\\-]+',
            }
        ),
    )
    username = forms.CharField(
        max_length=30,
        label='Имя пользователя',
        help_text='Не более 30 символов. Разрешены только латиница, цифры и _.',
        widget=forms.TextInput(
            attrs={
                'pattern': '[a-zA-Z0-9_]+',
            }
        ),
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError('Только латиница, цифры и тире разрешены.')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Это имя пользователя уже занято.')
        return username

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
