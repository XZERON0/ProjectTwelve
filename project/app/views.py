from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from auditlog.models import LogEntry
from . import models
def index(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    recent_operations = LogEntry.objects.filter(actor=request.user).order_by('-timestamp')
    context = {
        'recent_operations': recent_operations.first()  
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
    if not request.user.is_authenticated:
        return redirect('login')
    products = models.Product.objects.prefetch_related('stock_set').all()
    category = request.GET.get('category', '')
    name = request.GET.get('name', '')
    if category:
        products = products.filter(category=category)
    if name:
        products = products.filter(name__icontains=name)
    categories = models.Product.objects.values_list('category', flat=True).distinct()
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category,
        'search_name': name,
    }
    return render(request, 'goods/goods.html', context)

## Reports

