from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Category, Product, Promotion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from .models import Category 

# Create your views here.
def add_category(request):
    if request.method == 'POST':
        # Process the form data
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        
        # Create and save the new category
        Category.objects.create(name=name, slug=slug)
        messages.success(request, 'Category added successfully!')
        return redirect('dashboard:some_view')  # Redirect to an appropriate view
        
    return render(request, 'dashboard/add_category.html')

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    query = request.GET.get('q', '')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(loja__icontains=query)
        )
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    paginator = Paginator(products, 12)  # 12 produtos por página
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request,
                 'catalog/product/list.html',
                 {'category': category,
                  'categories': categories,
                  'products': products,
                  'query': query})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                               id=id,
                               slug=slug,
                               available=True)
    return render(request,
                 'catalog/product/detail.html',
                 {'product': product})

def home(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    query = request.GET.get('q', '')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(loja__icontains=query)
        )
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    paginator = Paginator(products, 12)  # 12 produtos por página
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request,
                 'catalog/home.html',
                 {'category': category,
                  'categories': categories,
                  'products': products,
                  'query': query})
