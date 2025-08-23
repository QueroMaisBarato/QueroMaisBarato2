"""
URL configuration for marketplace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from marketplace import views

# SEO Views
@cache_page(60 * 60 * 24)  # Cache for 24 hours
def sitemap_xml(request):
    with open('sitemap.xml', 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content, content_type='application/xml')

@cache_page(60 * 60 * 24)  # Cache for 24 hours
def robots_txt(request):
    with open('robots.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content, content_type='text/plain')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),  # <-- Coloque o dashboard ANTES do catálogo
    path('', include('catalog.urls', namespace='catalog')),
    
    # SEO URLs
    path('sitemap.xml', sitemap_xml, name='sitemap'),
    path('robots.txt', robots_txt, name='robots'),
    
    # Error pages
    path('error/<str:error_code>/', views.error_page, name='error_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
