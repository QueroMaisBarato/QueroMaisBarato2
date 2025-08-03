# Sistema de Tratamento de Erros - Django

Este sistema implementa um gerenciamento completo de erros para o Django, permitindo que você seja redirecionado para páginas de erro personalizadas quando ocorrerem problemas.

## 🚀 Funcionalidades

- ✅ **Páginas de erro personalizadas** para 400, 403, 404 e 500
- ✅ **Middleware automático** para capturar exceções
- ✅ **Templates responsivos** com design moderno
- ✅ **Logging automático** de erros para debugging
- ✅ **Suporte a AJAX** com respostas JSON
- ✅ **Redirecionamento automático** para páginas de erro apropriadas

## 📁 Estrutura de Arquivos

```
marketplace/
├── views.py                    # Views de erro personalizadas
├── middleware.py               # Middleware para captura de erros
├── templates/
│   └── errors/
│       ├── base_error.html     # Template base para erros
│       ├── 404.html           # Erro 404 - Página não encontrada
│       ├── 500.html           # Erro 500 - Erro interno do servidor
│       ├── 403.html           # Erro 403 - Acesso negado
│       ├── 400.html           # Erro 400 - Requisição inválida
│       └── error.html         # Template genérico para erros
└── urls.py                     # URLs para páginas de erro

examples/
└── error_handling_examples.py  # Exemplos de uso

ERROR_HANDLING_README.md        # Esta documentação
```

## ⚙️ Configuração

### 1. Settings.py

O sistema já está configurado no `settings.py`:

```python
# Error handling configuration
HANDLER404 = 'marketplace.views.handler404'
HANDLER500 = 'marketplace.views.handler500'
HANDLER403 = 'marketplace.views.handler403'
HANDLER400 = 'marketplace.views.handler400'

# Middleware para captura de erros
MIDDLEWARE = [
    # ... outros middlewares ...
    'marketplace.middleware.ErrorHandlingMiddleware',
    'marketplace.middleware.Custom404Middleware',
]
```

### 2. URLs

As URLs de erro já estão configuradas:

```python
# Error pages
path('error/<str:error_code>/', views.error_page, name='error_page'),
```

## 🎯 Como Usar

### 1. Tratamento Automático

O sistema funciona automaticamente! Quando ocorrer um erro, você será redirecionado para a página apropriada:

- **404**: Página não encontrada
- **500**: Erro interno do servidor
- **403**: Acesso negado
- **400**: Requisição inválida

### 2. Tratamento Manual em Views

```python
from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import ValidationError

def minha_view(request):
    try:
        # Sua lógica aqui
        produto = Produto.objects.get(id=123)
        return render(request, 'produto.html', {'produto': produto})
    
    except Produto.DoesNotExist:
        # Redireciona para página 404
        return redirect(reverse('error_page', kwargs={'error_code': '404'}))
    
    except ValidationError:
        # Redireciona para página 400
        return redirect(reverse('error_page', kwargs={'error_code': '400'}))
    
    except Exception as e:
        # Log do erro
        logger.error(f"Erro inesperado: {str(e)}")
        # Redireciona para página 500
        return redirect(reverse('error_page', kwargs={'error_code': '500'}))
```

### 3. Usando Decoradores

```python
from examples.error_handling_examples import handle_errors

@handle_errors
def minha_view_protegida(request, produto_id):
    # Se ocorrer qualquer erro, será tratado automaticamente
    produto = Produto.objects.get(id=produto_id)
    return render(request, 'produto.html', {'produto': produto})
```

### 4. Para APIs (JSON)

```python
from django.http import JsonResponse

def minha_api_view(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
        return JsonResponse({'produto': produto.nome})
    
    except Produto.DoesNotExist:
        return JsonResponse(
            {'error': '404', 'message': 'Produto não encontrado'},
            status=404
        )
```

## 🎨 Personalização

### 1. Modificar Mensagens de Erro

Edite o arquivo `marketplace/views.py`:

```python
def handler404(request, exception=None):
    context = {
        'error_code': '404',
        'error_title': 'Sua mensagem personalizada',
        'error_message': 'Sua descrição personalizada',
        'error_description': 'Sua instrução personalizada',
    }
    return render(request, 'errors/404.html', context, status=404)
```

### 2. Modificar Design

Edite o arquivo `marketplace/templates/errors/base_error.html`:

```html
<style>
    /* Seus estilos personalizados aqui */
    .error-container {
        background: #sua-cor;
        /* ... */
    }
</style>
```

### 3. Adicionar Novos Tipos de Erro

1. Crie uma nova view em `marketplace/views.py`:
```python
def handler401(request, exception=None):
    context = {
        'error_code': '401',
        'error_title': 'Não autorizado',
        'error_message': 'Você precisa fazer login para acessar esta página.',
        'error_description': 'Faça login e tente novamente.',
    }
    return render(request, 'errors/401.html', context, status=401)
```

2. Crie o template `marketplace/templates/errors/401.html`:
```html
{% extends 'errors/base_error.html' %}
{% block title %}Não autorizado - 401{% endblock %}
```

3. Adicione a URL:
```python
path('error/401/', views.handler401, name='error_401'),
```

## 🔧 Debugging

### 1. Logs Automáticos

O sistema registra automaticamente todos os erros. Verifique os logs do Django para ver detalhes dos erros.

### 2. Modo Debug

Quando `DEBUG = True` no `settings.py`, o Django mostrará páginas de erro detalhadas em vez das páginas personalizadas.

### 3. Testando Erros

Para testar as páginas de erro, acesse:
- `http://seu-site.com/error/404/`
- `http://seu-site.com/error/500/`
- `http://seu-site.com/error/403/`
- `http://seu-site.com/error/400/`

## 📱 Responsividade

As páginas de erro são totalmente responsivas e funcionam em:
- ✅ Desktop
- ✅ Tablet
- ✅ Mobile

## 🎯 Exemplos Práticos

### Exemplo 1: View com Validação

```python
def criar_produto(request):
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            if not nome:
                raise ValidationError('Nome é obrigatório')
            
            preco = request.POST.get('preco')
            if not preco or float(preco) <= 0:
                raise ValidationError('Preço deve ser maior que zero')
            
            # Salva o produto
            produto = Produto.objects.create(nome=nome, preco=preco)
            messages.success(request, 'Produto criado com sucesso!')
            return redirect('lista_produtos')
        
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect(reverse('error_page', kwargs={'error_code': '400'}))
        
        except Exception as e:
            logger.error(f"Erro ao criar produto: {str(e)}")
            return redirect(reverse('error_page', kwargs={'error_code': '500'}))
    
    return render(request, 'criar_produto.html')
```

### Exemplo 2: API com Tratamento de Erro

```python
def api_produto(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
        return JsonResponse({
            'id': produto.id,
            'nome': produto.nome,
            'preco': str(produto.preco)
        })
    
    except Produto.DoesNotExist:
        return JsonResponse({
            'error': '404',
            'message': 'Produto não encontrado'
        }, status=404)
    
    except Exception as e:
        logger.error(f"Erro na API: {str(e)}")
        return JsonResponse({
            'error': '500',
            'message': 'Erro interno do servidor'
        }, status=500)
```

## 🚨 Importante

1. **Em produção**: Certifique-se de que `DEBUG = False` no `settings.py`
2. **Logs**: Configure logging adequado para capturar erros
3. **Monitoramento**: Considere usar ferramentas como Sentry para monitoramento de erros
4. **Testes**: Teste todas as páginas de erro antes de fazer deploy

## 📞 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique os logs do Django
2. Teste as páginas de erro manualmente
3. Verifique se o middleware está configurado corretamente
4. Certifique-se de que os templates estão no local correto

---

**Sistema de Tratamento de Erros** - Criado para melhorar a experiência do usuário e facilitar o debugging de problemas no Django. 