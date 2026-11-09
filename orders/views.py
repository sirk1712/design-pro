from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

# просмотр главной страницы
def index(request):
    # пока здесь нет заявок, просто рендерим пустую страницу
    return render(request, 'orders/index.html')

# регистрация
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.surname = form.cleaned_data['surname']
            user.name = form.cleaned_data['name']
            user.patronymic = form.cleaned_data['patronymic']
            user.consent = form.cleaned_data['consent']

            # сохраняем пароль в зашифрованном виде
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'orders/register.html', {'form': form})

# вход в личный кабинет по логину и паролю
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # если это админ, кидаем в админку
            if user.is_superuser:
                return redirect('/superadmin/')
            return redirect('index') # обычного пользователя пока направляем на главную
        else:
            messages.error(request, "Неверный логин или пароль")
    else:
        form = AuthenticationForm()
    return render(request, 'orders/login.html', {'form': form})

# выход
def logout_view(request):
    logout(request)
    return redirect('index')

# личный кабинет (заглушка)
@login_required
def profile_view(request):
    return render(request, 'orders/profile.html')