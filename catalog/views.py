from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Category, Product
from django.db.models import Q
from django.template.loader import render_to_string

def home(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by('id').distinct('id')
    query = request.GET.get('q', '')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Log: total de produtos
    total_products = products.count()
    print(f"Total de produtos disponíveis: {total_products}")

    # Paginação manual
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except ValueError:
        page = 1
    offset = (page - 1) * 12
    products_page = products[offset:offset + 12]

    # Log: produtos na página
    product_ids = [p.id for p in products_page]
    product_names = [p.name for p in products_page]
    print(f"Produtos na página {page}: IDs={product_ids}, Names={product_names}")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(
            'catalog/product/_card.html',
            {'products': products_page},
            request=request
        )
        # Log: tamanho do HTML retornado
        print(f"Tamanho do HTML retornado na página {page}: {len(html)}")
        return JsonResponse({
            'html': html,
            'has_next': offset + 12 < total_products,
            'next_page': page + 1 if offset + 12 < total_products else None
        })

    return render(request,
                 'catalog/home.html',
                 {'category': category,
                  'categories': categories,
                  'products': products_page,
                  'query': query})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                               id=id,
                               slug=slug,
                               available=True)
    return render(request,
                 'catalog/product/detail.html',
                 {'product': product})