from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('categoria/<slug:category_slug>/', views.home, name='home_by_category'),
    path('produto/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]