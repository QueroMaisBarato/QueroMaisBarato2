from django.shortcuts import render
from django.http import Http404
from django.template import loader
from django.http import HttpResponse
from django.views.defaults import page_not_found, server_error, permission_denied, bad_request

def handler404(request, exception=None):
    """
    View personalizada para erro 404 - Página não encontrada
    """
    context = {
        'error_code': '404',
        'error_title': 'Página não encontrada',
        'error_message': 'A página que você está procurando não existe ou foi movida.',
        'error_description': 'Verifique se o endereço está correto ou volte para a página inicial.',
    }
    return render(request, 'errors/404.html', context, status=404)

def handler500(request, exception=None):
    """
    View personalizada para erro 500 - Erro interno do servidor
    """
    context = {
        'error_code': '500',
        'error_title': 'Erro interno do servidor',
        'error_message': 'Ocorreu um erro inesperado. Nossa equipe foi notificada.',
        'error_description': 'Tente novamente em alguns minutos ou entre em contato conosco.',
    }
    return render(request, 'errors/500.html', context, status=500)

def handler403(request, exception=None):
    """
    View personalizada para erro 403 - Acesso negado
    """
    context = {
        'error_code': '403',
        'error_title': 'Acesso negado',
        'error_message': 'Você não tem permissão para acessar esta página.',
        'error_description': 'Verifique suas credenciais ou entre em contato com o administrador.',
    }
    return render(request, 'errors/403.html', context, status=403)

def handler400(request, exception=None):
    """
    View personalizada para erro 400 - Requisição inválida
    """
    context = {
        'error_code': '400',
        'error_title': 'Requisição inválida',
        'error_message': 'A requisição enviada não é válida.',
        'error_description': 'Verifique os dados enviados e tente novamente.',
    }
    return render(request, 'errors/400.html', context, status=400)

def error_page(request, error_code='404'):
    """
    View genérica para páginas de erro
    """
    error_messages = {
        '404': {
            'title': 'Página não encontrada',
            'message': 'A página que você está procurando não existe ou foi movida.',
            'description': 'Verifique se o endereço está correto ou volte para a página inicial.',
        },
        '500': {
            'title': 'Erro interno do servidor',
            'message': 'Ocorreu um erro inesperado. Nossa equipe foi notificada.',
            'description': 'Tente novamente em alguns minutos ou entre em contato conosco.',
        },
        '403': {
            'title': 'Acesso negado',
            'message': 'Você não tem permissão para acessar esta página.',
            'description': 'Verifique suas credenciais ou entre em contato com o administrador.',
        },
        '400': {
            'title': 'Requisição inválida',
            'message': 'A requisição enviada não é válida.',
            'description': 'Verifique os dados enviados e tente novamente.',
        },
    }
    
    error_info = error_messages.get(error_code, error_messages['404'])
    
    context = {
        'error_code': error_code,
        'error_title': error_info['title'],
        'error_message': error_info['message'],
        'error_description': error_info['description'],
    }
    
    return render(request, 'errors/error.html', context, status=int(error_code)) 