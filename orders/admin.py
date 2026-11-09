from django.contrib import admin
from .models import CustomUser, Category, Order

# настройка отображения для пользователей
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'surname', 'name', 'email', 'is_staff')

# настройка отображения для категорий
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

# настройка отображения для заявок
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'status', 'created_at')
    list_filter = ('status', 'category')
