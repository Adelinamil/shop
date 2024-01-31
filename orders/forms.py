from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, HiddenInput

from orders.models import Order


class OrderForm(ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=HiddenInput())
    password = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')

    class Meta:
        model = Order
        fields = ['user', 'address', 'postal_code', 'city']
