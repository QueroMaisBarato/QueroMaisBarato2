from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Category, Product, Promotion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.template.loader import render_to_string

def home(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by('id').distinct('id')  # Unicidade por ID
    query = request.GET.get('q', '')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    paginator = Paginator(products, 12)  # 12 produtos por página
    page = request.GET.get('page', 1)
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Log para depuração
        print(f"Produtos na página {page}: {[p.id for p in products_page]}")
        # Requisição AJAX: retorna apenas o HTML dos produtos
        html = render_to_string(
            'catalog/product/_card.html',
            {'products': products_page},
            request=request
        )
        return JsonResponse({
            'html': html,
            'has_next': products_page.has_next(),
            'next_page': products_page.next_page_number() if products_page.has_next() else None
        })

    # Log para depuração na carga inicial
    print(f"Produtos na página inicial {page}: {[p.id for p in products_page]}")
    return render(request,
                 'catalog/home.html',
                 {'category': category,
                  'categories': categories,
                  'products': products_page,
                  'query': query})

def product_list(request, category_slug=None):
    return home(request, category_slug)

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                               id=id,
                               slug=slug,
                               available=True)
    return render(request,
                 'catalog/product/detail.html',
                 {'product': product})