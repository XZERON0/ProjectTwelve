from django.shortcuts import render
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'reqister.html')

