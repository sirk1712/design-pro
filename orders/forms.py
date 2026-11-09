from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

from .models import Order


# получаем нашу кастомную модель
User = get_user_model()

# форма регистрации
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Повтор пароля")

    email = forms.EmailField(label="Email", required=True)
    surname = forms.CharField(label="Фамилия", max_length=100)
    name = forms.CharField(label="Имя", max_length=100)
    patronymic = forms.CharField(label="Отчество", max_length=100, required=False)
    consent = forms.BooleanField(label="Согласие на обработку персональных данных", required=True)

    class Meta:
        model = User
        fields = ['surname', 'name', 'patronymic', 'username', 'email']

    # валидация ФИО
    def clean_surname(self):
        data = self.cleaned_data['surname']
        if not re.match(r'^[А-Яа-яЁё\s\-]+$', data):
            raise ValidationError("Фамилия должна содержать только кириллические буквы, дефис и пробелы.")
        return data

    def clean_name(self):
        data = self.cleaned_data['name']
        if not re.match(r'^[А-Яа-яЁё\s\-]+$', data):
            raise ValidationError("Имя должно содержать только кириллические буквы, дефис и пробелы.")
        return data

    def clean_patronymic(self):
        data = self.cleaned_data['patronymic']
        if data and not re.match(r'^[А-Яа-яЁё\s\-]+$', data):
            raise ValidationError("Отчество должно содержать только кириллические буквы, дефис и пробелы.")
        return data

    # валидация логина
    def clean_username(self):
        data = self.cleaned_data['username']
        if not re.match(r'^[A-Za-z\-]+$', data):
            raise ValidationError("Логин должен содержать только латиницу и дефис.")
        if User.objects.filter(username=data).exists():
            raise ValidationError("Этот логин уже занят.")
        return data

    # проверка совпадения паролей
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Пароли не совпадают.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # применяем стили Bootstrap
        for field_name, field in self.fields.items():
            # если это чекбокс -> form-check-input
            if field_name == 'consent':
                field.widget.attrs.update({'class': 'form-check-input'})
            # для всех остальных полей -> form-control
            else:
                field.widget.attrs.update({'class': 'form-control'})

# форма для создания заявки
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title', 'description', 'category', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            # проверяем размер изображения (2 Мб)
            if photo.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Размер файла не должен превышать 2Мб.")

            # проверяем расширения изображения
            valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
            import os
            ext = os.path.splitext(photo.name)[1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError("Допустимые форматы: jpg, jpeg, png, bmp.")
        return photo