# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from base.models import Customer


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Customer
        fields = ('username', 'password')

class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
            visible.field.label = 'col-form-label'

    class Meta:
        model = Customer
        fields = ('username', 'password1', 'password2')
