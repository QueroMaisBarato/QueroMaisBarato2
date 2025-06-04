#!/bin/bash

# Ativar ambiente virtual (se estiver usando)
# source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Carregar dados iniciais
python load_initial_data.py

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Iniciar o servidor (ajuste conforme seu ambiente de produção)
# python manage.py runserver 0.0.0.0:8000 