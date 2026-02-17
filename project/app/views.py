from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from auditlog.models import LogEntry
def index(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    all_log = LogEntry.objects.filter(actor=request.user).order_by('-action_time')
    for entry in all_log:
        print(f"Действие: {entry.get_action_display()}") # Создание/Изменение/Удаление
        print(f"Объект: {entry.content_type.name}")      # Тип (например, Продукт)
        print(f"Название: {entry.object_repr}")          # Имя (например, "Чай")
        print(f"Дата: {entry.timestamp}")
    context = {
        'all_log': all_log  
    }
    return render(request, 'index.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            User.objects.filter(username=username).update(is_staff=True)
            return redirect('index', )
    form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    if request.method =='POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login')
    form = AuthenticationForm()
    print(form.errors)
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('index')

## Goods
def goods(request):
    return render(request, 'goods/goods.html')