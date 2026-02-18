from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from auditlog.models import LogEntry
from . import models
@login_required
def index(request):
    recent_operations = LogEntry.objects.filter(actor=request.user).order_by('-timestamp')[:20]
    context = {
        'recent_operations': recent_operations,
        'total_products': models.Product.objects.count(),
        'categories' : models.Product.objects.values_list('category', flat=True).distinct().count(),
        'low_stock' : models.Stock.objects.filter(quantity__lte=5).count(),
        'total_value': sum([(income.price * income.quantity) for income in models.Income.objects.all()])
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
@login_required
def goods(request):
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
@login_required
def suppliers(request):
    if not request.user.is_authenticated:
        return redirect('login')
    suppliers = models.Supplier.objects.all()
    context = {
        'suppliers': suppliers,
    }
    return render(request, 'suppliers.html', context)