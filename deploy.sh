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


python manage.py migrate && \
python manage.py collectstatic --noinput && \
echo \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='queromaisbarato.email@gmail.com').exists() or User.objects.create_superuser('admin', 'queromaisbarato.email@gmail.com', '135246@@aA')\" | python manage.py shell && \
gunicorn marketplace.wsgi:application --bind 0.0.0.0:10000