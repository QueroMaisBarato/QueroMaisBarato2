from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import Category, Product
from .forms import ProductForm, CategoryForm

@login_required
def home(request):
    context = {
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'available_products': Product.objects.filter(available=True).count(),
        'pix_products': Product.objects.filter(pix=True).count(),
        'latest_products': Product.objects.select_related('category').order_by('-created')[:5]
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def category_list(request):
    categories = Category.objects.all().order_by('order')
    return render(request, 'dashboard/category_list.html', {'categories': categories})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria adicionada com sucesso!')
            return redirect('dashboard:category_list')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = CategoryForm()

    return render(request, 'dashboard/category_form.html', {'form': form, 'action': 'Adicionar'})

@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('dashboard:category_list')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'dashboard/category_form.html', {'form': form, 'action': 'Editar'})

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('dashboard:category_list')
    return render(request, 'dashboard/category_confirm_delete.html', {'category': category})

@login_required
def product_list(request):
    products = Product.objects.all().select_related('category')
    return render(request, 'dashboard/product_list.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto adicionado com sucesso!')
            return redirect('dashboard:product_list')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = ProductForm()

    return render(request, 'dashboard/product_form.html', {'form': form, 'action': 'Adicionar'})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('dashboard:product_list')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = ProductForm(instance=product)

    return render(request, 'dashboard/product_form.html', {'form': form, 'action': 'Editar'})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('dashboard:product_list')
    return render(request, 'dashboard/product_confirm_delete.html', {'product': product})

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


