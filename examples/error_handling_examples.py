"""
Exemplos de como usar o sistema de tratamento de erros no Django

Este arquivo mostra diferentes formas de implementar tratamento de erros
em suas views Django.
"""

from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.core.exceptions import PermissionDenied, ValidationError
from django.urls import reverse
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

# Exemplo 1: Tratamento básico de erro com try/except
def exemplo_view_basica(request, product_id):
    """
    Exemplo básico de tratamento de erro usando try/except
    """
    try:
        # Simula uma operação que pode falhar
        product = Product.objects.get(id=product_id)
        return render(request, 'product_detail.html', {'product': product})
    
    except Product.DoesNotExist:
        # Log do erro para debugging
        logger.warning(f"Produto com ID {product_id} não encontrado")
        
        # Adiciona mensagem para o usuário
        messages.error(request, 'Produto não encontrado.')
        
        # Redireciona para página de erro personalizada
        return redirect(reverse('error_page', kwargs={'error_code': '404'}))
    
    except Exception as e:
        # Log de erro inesperado
        logger.error(f"Erro inesperado ao buscar produto {product_id}: {str(e)}")
        
        # Redireciona para página de erro 500
        return redirect(reverse('error_page', kwargs={'error_code': '500'}))

# Exemplo 2: Usando decoradores para tratamento de erro
from functools import wraps
from django.http import JsonResponse

def handle_errors(view_func):
    """
    Decorador para tratamento automático de erros
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        
        except Http404:
            return redirect(reverse('error_page', kwargs={'error_code': '404'}))
        
        except PermissionDenied:
            return redirect(reverse('error_page', kwargs={'error_code': '403'}))
        
        except ValidationError as e:
            messages.error(request, f'Dados inválidos: {str(e)}')
            return redirect(reverse('error_page', kwargs={'error_code': '400'}))
        
        except Exception as e:
            logger.error(f"Erro inesperado em {view_func.__name__}: {str(e)}")
            return redirect(reverse('error_page', kwargs={'error_code': '500'}))
    
    return wrapper

@handle_errors
def exemplo_view_com_decorador(request, product_id):
    """
    Exemplo usando decorador para tratamento automático de erros
    """
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# Exemplo 3: Tratamento de erro para APIs (JSON)
def exemplo_api_view(request, product_id):
    """
    Exemplo de tratamento de erro para APIs que retornam JSON
    """
    try:
        product = Product.objects.get(id=product_id)
        data = {
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
        }
        return JsonResponse(data)
    
    except Product.DoesNotExist:
        return JsonResponse(
            {'error': '404', 'message': 'Produto não encontrado'},
            status=404
        )
    
    except Exception as e:
        logger.error(f"Erro na API para produto {product_id}: {str(e)}")
        return JsonResponse(
            {'error': '500', 'message': 'Erro interno do servidor'},
            status=500
        )

# Exemplo 4: View com validação personalizada
def exemplo_view_com_validacao(request):
    """
    Exemplo de view com validação personalizada e tratamento de erro
    """
    if request.method == 'POST':
        try:
            # Validação dos dados
            name = request.POST.get('name')
            if not name or len(name.strip()) < 3:
                raise ValidationError('Nome deve ter pelo menos 3 caracteres')
            
            price = request.POST.get('price')
            if not price or float(price) <= 0:
                raise ValidationError('Preço deve ser maior que zero')
            
            # Processa os dados válidos
            # ... lógica de processamento ...
            
            messages.success(request, 'Produto criado com sucesso!')
            return redirect('product_list')
        
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect(reverse('error_page', kwargs={'error_code': '400'}))
        
        except ValueError:
            messages.error(request, 'Dados inválidos fornecidos')
            return redirect(reverse('error_page', kwargs={'error_code': '400'}))
        
        except Exception as e:
            logger.error(f"Erro ao criar produto: {str(e)}")
            return redirect(reverse('error_page', kwargs={'error_code': '500'}))
    
    return render(request, 'create_product.html')

# Exemplo 5: Middleware personalizado para logging
class LoggingMiddleware:
    """
    Exemplo de middleware para logging de erros
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """
        Log de todas as exceções não tratadas
        """
        logger.error(f"""
        Exceção não tratada:
        URL: {request.path}
        Método: {request.method}
        Usuário: {request.user}
        Exceção: {type(exception).__name__}
        Mensagem: {str(exception)}
        """)
        return None

# Exemplo 6: Função utilitária para tratamento de erro
def safe_get_object_or_404(model, **kwargs):
    """
    Função utilitária que combina get_object_or_404 com logging
    """
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        logger.warning(f"Objeto {model.__name__} não encontrado com filtros: {kwargs}")
        raise Http404(f"{model.__name__} não encontrado")

# Exemplo 7: View usando a função utilitária
def exemplo_view_utilitaria(request, product_id):
    """
    Exemplo usando função utilitária para tratamento de erro
    """
    try:
        product = safe_get_object_or_404(Product, id=product_id, available=True)
        return render(request, 'product_detail.html', {'product': product})
    
    except Http404:
        messages.warning(request, 'Produto não encontrado ou indisponível')
        return redirect(reverse('error_page', kwargs={'error_code': '404'})) 