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

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('done', 'Выполнено'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    photo = models.ImageField(upload_to='orders_photos/', verbose_name="Фото помещения")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Временная метка")

    admin_comment = models.TextField(blank=True, null=True, verbose_name="Комментарий администратора")
    design_photo = models.ImageField(upload_to='design_photos/', blank=True, null=True, verbose_name="Фото готового дизайна")

    class Meta:
        ordering = ['-created_at']  # Сначала новые
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"