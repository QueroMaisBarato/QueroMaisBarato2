from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Category, Product
from django.db.models import Q

def home(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by('id')  # Removido distinct('id') para teste
    query = request.GET.get('q', '')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    total_products = products.count()
    print(f"Total de produtos disponíveis: {total_products}")

    page = request.GET.get('page', 1)
    try:
        page = int(page)
        print(f"Página solicitada: {page} (convertido de {request.GET.get('page')})")
    except ValueError:
        page = 1
        print(f"Página inválida, usando padrão: {page}")
    offset = (page - 1) * 12
    print(f"Offset calculado para página {page}: {offset}")
    products_page = products[offset:offset + 12]

    product_ids = [p.id for p in products_page]
    product_names = [p.name for p in products_page]
    print(f"Produtos na página {page}: Offset={offset}, IDs={product_ids}, Names={product_names}")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = ""
        for product in products_page:
            html += f'<div class="product-card" data-product-id="{product.id}">Produto: {product.name} (ID: {product.id})</div>'
        print(f"HTML gerado na página {page}: {len(html)} caracteres, {html.count('product-card')} produtos")
        return JsonResponse({
            'html': html,
            'has_next': offset + 12 < total_products,
            'next_page': page + 1 if offset + 12 < total_products else None
        })

    context = {
        'category': category,
        'categories': categories,
        'products': products_page,
        'query': query,
        'products_has_next': offset + 12 < total_products,
    }
    return render(request, 'catalog/home.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                               id=id,
                               slug=slug,
                               available=True)
    return render(request,
                 'catalog/product/detail.html',
                 {'product': product})