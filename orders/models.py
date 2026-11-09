from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    # убираем стандартные поля, чтобы использовать свои
    first_name = None
    last_name = None

    # добавляем свои поля
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    consent = models.BooleanField(default=False, verbose_name="Согласие на обработку персональных данных")

    def __str__(self):
        return f"{self.surname} {self.name} ({self.username})"
