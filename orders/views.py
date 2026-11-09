from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm

# просмотр главной страницы
def index(request):
    return render(request, 'orders/index.html')

# Вход в личный кабинет по логину и паролю
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # если это админ, направляем в админку
            if user.is_superuser:
                return redirect('/superadmin/')
            return redirect('index') # обычного пользователя направляем на главную
        else:
            messages.error(request, "Неверный логин или пароль")
    else:
        form = AuthenticationForm()
    return render(request, 'orders/login.html', {'form': form})
