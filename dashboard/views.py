from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import Category
from .forms import ProductForm
from .forms import CategoryForm

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria adicionada com sucesso!')
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = CategoryForm()

    return render(request, 'dashboard/add_category.html', {'form': form})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto adicionado com sucesso!')
            return redirect('dashboard:home')  # ajuste conforme sua estrutura
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = ProductForm()

    return render(request, 'dashboard/add_product.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:home')
        else:
            return render(request, 'dashboard/login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'dashboard/login.html')

def logout_view(request):
    logout(request)
    return redirect('dashboard:login')

@login_required
def home(request):
    return render(request, 'dashboard/home.html')


