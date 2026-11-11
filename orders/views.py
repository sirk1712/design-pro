from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm, OrderForm
from .models import Order, Category

# просмотр главной страницы
def index(request):
    # берем 4 последние выполненные заявки и считаем, сколько заявок в работе
    completed_orders = Order.objects.filter(status='done').order_by('-created_at')[:4]
    in_progress_count = Order.objects.filter(status='in_progress').count()

    context = {
        'completed_orders': completed_orders,
        'in_progress_count': in_progress_count
    }
    return render(request, 'orders/index.html', context)

# проверка, что вошедший пользователь - админ
def is_admin(user):
    return user.is_authenticated and user.is_superuser

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

# личный кабинет
@login_required
def profile_view(request):
    return render(request, 'orders/profile.html')

# создание заявки
@login_required
def create_order(request):
    # если пользователь - админ, не даем ему создавать заявку
    if request.user.is_superuser:
        messages.error(request, "Администраторы не могут создавать заявки.")
        return redirect('profile')

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user # привязываем к текущему пользователю
            # статус 'new' ставится автоматически в модели
            order.save()
            messages.success(request, "Заявка успешно создана!")
            return redirect('profile')
    else:
        form = OrderForm()
    return render(request, 'orders/create_order.html', {'form': form})


# просмотр заявок (с фильтрацией)
@login_required
def profile_view(request):
    # если зашел админ, то направляем его на панель управления
    if request.user.is_superuser:
        return redirect('admin_panel')

    # логика для обычного пользователя
    # берем заявки только текущего пользователя, сортируем по дате (новые сверху)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # фильтрация по статусу
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)

    return render(request, 'orders/profile.html', {'orders': orders})

# удаление заявки
@login_required
def delete_order(request, pk):
    # ищем заявку только среди заявок текущего пользователя
    order = get_object_or_404(Order, pk=pk, user=request.user)

    # проверяем, что статус заявки "Новая" (ее еще не взяли в работу)
    if order.status != 'new':
        messages.error(request, "Вы не можете удалить заявку, которую уже взяли в работу или выполнили.")
        return redirect('profile')

    if request.method == 'POST':
        order.delete()
        messages.success(request, "Заявка удалена.")
        return redirect('profile')

    # если это GET-запрос, показываем страницу подтверждения
    return render(request, 'orders/delete_confirm.html', {'order': order})

# страница панели управления заявками для админа
@user_passes_test(is_admin, login_url='/login/')
def admin_panel(request):
    # берем все заявки из базы и сортируем по дате
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders/admin_panel.html', {'orders': orders})


# изменение статуса заявки на "в работе" (принимает id заявки и новый статус)
@user_passes_test(is_admin, login_url='/login/')
def set_in_progress(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status != 'new':
        return redirect('admin_panel')

    if request.method == 'POST':
        comment = request.POST.get('comment')
        if comment:
            order.status = 'in_progress'
            order.admin_comment = comment
            order.save()
            messages.success(request, "Заявка переведена в работу.")
            return redirect('admin_panel')
        else:
            messages.error(request, "Необходимо оставить комментарий.")

    return render(request, 'orders/admin_set_in_progress.html', {'order': order})

# изменение статуса заявки на "выполнено" (принимает id заявки и новый статус)
@user_passes_test(is_admin, login_url='/login/')
def set_done(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status != 'new':
        return redirect('admin_panel')

    if request.method == 'POST':
        design_photo = request.FILES.get('design_photo')
        if design_photo:
            order.status = 'done'
            order.design_photo = design_photo
            order.save()
            messages.success(request, "Заявка выполнена.")
            return redirect('admin_panel')
        else:
            messages.error(request, "Необходимо прикрепить фото готового дизайна.")

    return render(request, 'orders/admin_set_done.html', {'order': order})

# управление категориями
@user_passes_test(is_admin, login_url='/login/')
def admin_categories(request):
    categories = Category.objects.all()
    return render(request, 'orders/admin_categories.html', {'categories': categories})

# добавление категории
@user_passes_test(is_admin, login_url='/login/')
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            return redirect('admin_categories')
    return render(request, 'orders/add_category.html')

# удаление категории (с удалением всех её заявок)
@user_passes_test(is_admin, login_url='/login/')
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete() # заявки удалятся автоматически
        return redirect('admin_categories')
    return render(request, 'orders/delete_category.html', {'category': category})