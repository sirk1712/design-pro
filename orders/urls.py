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
    path('admin-panel/status/<int:pk>/<str:new_status>/', views.change_status, name='change_status'),

    path('admin-panel/categories/', views.admin_categories, name='admin_categories'),
]