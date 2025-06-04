import os
import django
import json
from django.core import serializers
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

from catalog.models import Category, Product

def export_data():
    # Criar diretório para os dados se não existir
    os.makedirs('fixtures', exist_ok=True)
    
    # Exportar categorias
    categories = Category.objects.all()
    categories_data = serializers.serialize('json', categories)
    with open('fixtures/categories.json', 'w', encoding='utf-8') as f:
        f.write(categories_data)
    
    # Exportar produtos
    products = Product.objects.all()
    products_data = serializers.serialize('json', products)
    with open('fixtures/products.json', 'w', encoding='utf-8') as f:
        f.write(products_data)
    
    # Copiar imagens para pasta fixtures
    os.makedirs('fixtures/media', exist_ok=True)
    for product in products:
        if product.image:
            # Obter o caminho relativo da imagem
            image_path = product.image.name
            # Copiar a imagem para a pasta fixtures
            if default_storage.exists(image_path):
                with default_storage.open(image_path, 'rb') as source:
                    with open(f'fixtures/media/{os.path.basename(image_path)}', 'wb') as dest:
                        dest.write(source.read())
    
    print("Dados exportados com sucesso para a pasta 'fixtures'!")
    print(f"Total de categorias exportadas: {categories.count()}")
    print(f"Total de produtos exportados: {products.count()}")

if __name__ == '__main__':
    export_data() 