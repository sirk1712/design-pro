from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    path('order/create/', views.create_order, name='create_order'),
    path('order/<int:pk>/delete/', views.delete_order, name='delete_order'),

    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/status/<int:pk>/in-progress/', views.set_in_progress, name='set_in_progress'),
    path('admin-panel/status/<int:pk>/done/', views.set_done, name='set_done'),

    path('admin-panel/categories/', views.admin_categories, name='admin_categories'),
    path('admin-panel/categories/add/', views.add_category, name='add_category'),
    path('admin-panel/categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
]