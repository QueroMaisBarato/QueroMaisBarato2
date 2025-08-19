from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Category, Product, Promotion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from .models import Category 

# Create your views here.

def get_page_range(page_obj, max_pages=3):
    """
    Retorna um range de páginas para mostrar na paginação.
    Mostra no máximo max_pages páginas ao redor da página atual.
    """
    current_page = page_obj.number
    total_pages = page_obj.paginator.num_pages
    
    if total_pages <= max_pages:
        # Se temos poucas páginas, mostra todas
        return range(1, total_pages + 1)
    
    # Calcula o range de páginas para mostrar
    half_pages = max_pages // 2
    
    start_page = max(1, current_page - half_pages)
    end_page = min(total_pages, current_page + half_pages)
    
    # Ajusta o range se estamos nas bordas
    if start_page == 1:
        end_page = min(total_pages, start_page + max_pages - 1)
    elif end_page == total_pages:
        start_page = max(1, end_page - max_pages + 1)
    
    return range(start_page, end_page + 1)

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
    
    paginator = Paginator(products, 15)  # 12 produtos por página
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # Adiciona o range de páginas ao contexto
    page_range = get_page_range(products)

    return render(request,
                 'catalog/product/list.html',
                 {'category': category,
                  'categories': categories,
                  'products': products,
                  'query': query,
                  'page_range': page_range})

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

    # Adiciona o range de páginas ao contexto
    page_range = get_page_range(products)

    return render(request,
                 'catalog/home.html',
                 {'category': category,
                  'categories': categories,
                  'products': products,
                  'query': query,
                  'page_range': page_range})
