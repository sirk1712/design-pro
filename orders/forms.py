from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Повтор пароля")
    first_name = forms.CharField(label="ФИО", max_length=150)
    agree = forms.BooleanField(label="Согласие на обработку персональных данных")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        # Только кириллица, дефис и пробел
        if not re.match(r'^[А-Яа-яЁё\s\-]+$', data):
            raise ValidationError("ФИО должно содержать только кириллические буквы, дефис и пробелы.")
        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        # Только латиница и дефис
        if not re.match(r'^[A-Za-z\-]+$', data):
            raise ValidationError("Логин должен содержать только латиницу и дефис.")
        if User.objects.filter(username=data).exists():
            raise ValidationError("Этот логин уже занят.")
        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Пароли не совпадают.")
        return cleaned_data