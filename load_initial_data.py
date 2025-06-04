import os
import django
from django.core.management import call_command
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

def load_initial_data():
    # Carregar fixtures
    fixtures_dir = 'fixtures'
    
    # Carregar categorias
    if os.path.exists(os.path.join(fixtures_dir, 'categories.json')):
        call_command('loaddata', os.path.join(fixtures_dir, 'categories.json'))
        print("Categorias carregadas com sucesso!")
    
    # Carregar produtos
    if os.path.exists(os.path.join(fixtures_dir, 'products.json')):
        call_command('loaddata', os.path.join(fixtures_dir, 'products.json'))
        print("Produtos carregados com sucesso!")
    
    # Copiar imagens para a pasta media
    media_dir = os.path.join(fixtures_dir, 'media')
    if os.path.exists(media_dir):
        for filename in os.listdir(media_dir):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                source_path = os.path.join(media_dir, filename)
                with open(source_path, 'rb') as f:
                    default_storage.save(f'products/{filename}', ContentFile(f.read()))
        print("Imagens copiadas com sucesso!")

if __name__ == '__main__':
    load_initial_data() 