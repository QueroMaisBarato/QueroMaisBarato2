import os
import django
import json
import shutil
from django.core import serializers
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.management import call_command
from django.conf import settings

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

from catalog.models import Category, Product

def export_data():
    print("Iniciando exportação dos dados...")
    
    # Criar diretório para os dados se não existir
    os.makedirs('fixtures', exist_ok=True)
    
    # Exportar categorias
    categories = Category.objects.all()
    categories_data = serializers.serialize('json', categories, ensure_ascii=False)
    with open('fixtures/categories.json', 'w', encoding='utf-8') as f:
        f.write(categories_data)
    print(f"✓ {categories.count()} categorias exportadas")
    
    # Exportar produtos
    products = Product.objects.all()
    products_data = serializers.serialize('json', products, ensure_ascii=False)
    with open('fixtures/products.json', 'w', encoding='utf-8') as f:
        f.write(products_data)
    print(f"✓ {products.count()} produtos exportados")
    
    # Copiar imagens para pasta fixtures
    media_dir = os.path.join(settings.MEDIA_ROOT)
    fixtures_media_dir = os.path.join('fixtures', 'media')
    os.makedirs(fixtures_media_dir, exist_ok=True)
    
    images_count = 0
    for product in products:
        if product.image:
            # Obter o caminho relativo da imagem
            image_path = product.image.name
            # Caminho completo da imagem original
            source_path = os.path.join(media_dir, image_path)
            # Caminho de destino na pasta fixtures
            dest_path = os.path.join(fixtures_media_dir, os.path.basename(image_path))
            
            # Copiar o arquivo se existir
            if os.path.exists(source_path):
                shutil.copy2(source_path, dest_path)
                images_count += 1
                print(f"Copiando imagem: {image_path}")
            else:
                print(f"Aviso: Imagem não encontrada: {source_path}")
    
    print(f"✓ {images_count} imagens exportadas")
    
    print("\nExportação concluída com sucesso!")
    return True

def import_data():
    print("\nIniciando importação dos dados...")
    
    try:
        # Limpar dados existentes
        Product.objects.all().delete()
        Category.objects.all().delete()
        print("✓ Dados antigos removidos")
        
        # Carregar categorias
        if os.path.exists('fixtures/categories.json'):
            with open('fixtures/categories.json', 'r', encoding='utf-8') as f:
                categories_data = f.read()
            for obj in serializers.deserialize('json', categories_data):
                obj.save()
            print("✓ Categorias importadas")
        
        # Carregar produtos
        if os.path.exists('fixtures/products.json'):
            with open('fixtures/products.json', 'r', encoding='utf-8') as f:
                products_data = f.read()
            for obj in serializers.deserialize('json', products_data):
                obj.save()
            print("✓ Produtos importados")
        
        # Copiar imagens para a pasta media
        media_dir = os.path.join(settings.MEDIA_ROOT)
        fixtures_media_dir = os.path.join('fixtures', 'media')
        
        if os.path.exists(fixtures_media_dir):
            images_count = 0
            for filename in os.listdir(fixtures_media_dir):
                if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    source_path = os.path.join(fixtures_media_dir, filename)
                    dest_path = os.path.join(media_dir, 'products', filename)
                    
                    # Garantir que o diretório de destino existe
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    
                    # Copiar o arquivo
                    shutil.copy2(source_path, dest_path)
                    images_count += 1
                    print(f"Copiando imagem: {filename}")
            print(f"✓ {images_count} imagens importadas")
        
        print("\nImportação concluída com sucesso!")
        return True
        
    except Exception as e:
        print(f"\nErro durante a importação: {str(e)}")
        return False

def deploy_data():
    print("=== INICIANDO PROCESSO DE DEPLOY DOS DADOS ===\n")
    
    # Exportar dados do ambiente atual
    if not export_data():
        print("Erro na exportação dos dados!")
        return False
    
    # Aqui você pode adicionar comandos para fazer backup dos dados
    # antes de importar no novo ambiente
    
    # Importar dados no novo ambiente
    if not import_data():
        print("Erro na importação dos dados!")
        return False
    
    print("\n=== DEPLOY DOS DADOS CONCLUÍDO COM SUCESSO! ===")
    return True

if __name__ == '__main__':
    deploy_data() 