# Guia de Deploy

Este guia explica como fazer o deploy do projeto, incluindo a migração dos dados.

## Pré-requisitos

1. Python 3.8 ou superior instalado
2. Ambiente virtual configurado
3. Dependências do projeto instaladas (`pip install -r requirements.txt`)
4. Acesso ao servidor de destino

## Processo de Deploy

### 1. Preparação do Ambiente

```bash
# Criar e ativar ambiente virtual (se ainda não existir)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Backup dos Dados (Ambiente Atual)

```bash
# Fazer backup do banco de dados atual
python manage.py dumpdata > backup.json

# Exportar dados e mídia
python deploy_data.py
```

### 3. Deploy do Código

```bash
# 1. Fazer push do código para o repositório
git add .
git commit -m "Preparando deploy"
git push origin main

# 2. No servidor de destino, fazer pull do código
git pull origin main
```

### 4. Configuração do Ambiente de Destino

```bash
# 1. Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente
# Copiar .env.example para .env e ajustar as configurações
cp .env.example .env
```

### 5. Migração do Banco de Dados

```bash
# 1. Aplicar migrações
python manage.py migrate

# 2. Importar dados
python deploy_data.py
```

### 6. Configuração do Servidor Web

1. Configurar o servidor web (Nginx/Apache) para servir os arquivos estáticos e mídia
2. Configurar o servidor WSGI (Gunicorn/uWSGI)
3. Configurar o serviço do sistema (systemd/supervisor)

### 7. Verificação Final

1. Verificar se todas as rotas estão funcionando
2. Testar o upload de imagens
3. Verificar se os dados foram importados corretamente
4. Testar a busca e filtros de produtos

## Estrutura de Arquivos Importante

```
projeto/
├── fixtures/              # Dados exportados
│   ├── categories.json    # Categorias
│   ├── products.json      # Produtos
│   └── media/            # Imagens dos produtos
├── deploy_data.py        # Script de deploy
└── DEPLOY.md            # Este guia
```

## Solução de Problemas

### Problemas Comuns

1. **Erro de permissão nas pastas de mídia**
   ```bash
   chmod -R 755 media/
   ```

2. **Erro ao importar dados**
   - Verificar se os arquivos JSON estão no formato correto
   - Verificar se as imagens estão na pasta correta

3. **Erro de conexão com o banco de dados**
   - Verificar as configurações no arquivo .env
   - Verificar se o banco de dados está acessível

### Logs

- Verificar os logs do servidor web
- Verificar os logs do Django (`python manage.py runserver` em modo debug)
- Verificar os logs do banco de dados

## Contato

Em caso de problemas, entre em contato com a equipe de desenvolvimento. 