import os
import django
import json
import sys
from django.core import serializers
from django.core.management import call_command
from io import StringIO
import codecs

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

def backup_database():
    print("Iniciando backup do banco de dados...")
    
    try:
        # Criar diretório para backup se não existir
        os.makedirs('backups', exist_ok=True)
        
        # Configurar encoding para UTF-8
        if sys.platform == 'win32':
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
        
        # Capturar a saída do dumpdata em um buffer
        buffer = StringIO()
        call_command('dumpdata', stdout=buffer)
        data = buffer.getvalue()
        
        # Salvar o backup com encoding UTF-8
        backup_file = 'backups/backup.json'
        with codecs.open(backup_file, 'w', encoding='utf-8') as f:
            f.write(data)
        
        print(f"✓ Backup criado com sucesso em: {backup_file}")
        return True
        
    except Exception as e:
        print(f"\nErro durante o backup: {str(e)}")
        return False

def restore_database():
    print("\nIniciando restauração do banco de dados...")
    
    try:
        backup_file = 'backups/backup.json'
        if not os.path.exists(backup_file):
            print(f"Arquivo de backup não encontrado: {backup_file}")
            return False
        
        # Limpar o banco de dados atual
        call_command('flush', '--no-input')
        print("✓ Banco de dados atual limpo")
        
        # Restaurar o backup
        with codecs.open(backup_file, 'r', encoding='utf-8') as f:
            data = f.read()
        
        # Deserializar e salvar os objetos
        for obj in serializers.deserialize('json', data):
            obj.save()
        
        print("✓ Backup restaurado com sucesso!")
        return True
        
    except Exception as e:
        print(f"\nErro durante a restauração: {str(e)}")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'restore':
        restore_database()
    else:
        backup_database() 