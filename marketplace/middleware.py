import logging
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
import traceback

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware:
    """
    Middleware para capturar exceções e redirecionar para páginas de erro personalizadas
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Captura erros 404 e redireciona para página personalizada
        if response.status_code == 404:
            return redirect(reverse('error_page', kwargs={'error_code': '404'}))
        
        return response

    def process_exception(self, request, exception):
        """
        Processa exceções não tratadas e redireciona para páginas de erro apropriadas
        """
        # Log da exceção para debugging
        logger.error(f"Exceção capturada: {type(exception).__name__}: {str(exception)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Mapeamento de exceções para códigos de erro
        error_mapping = {
            Http404: '404',
            PermissionDenied: '403',
            ValidationError: '400',
        }
        
        # Determina o código de erro baseado no tipo de exceção
        error_code = error_mapping.get(type(exception), '500')
        
        # Se for uma requisição AJAX, retorna JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return HttpResponse(
                f'{{"error": "{error_code}", "message": "Ocorreu um erro. Tente novamente."}}',
                content_type='application/json',
                status=int(error_code)
            )
        
        # Redireciona para a página de erro apropriada
        return redirect(reverse('error_page', kwargs={'error_code': error_code}))

 