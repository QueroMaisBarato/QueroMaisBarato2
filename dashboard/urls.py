from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_product/', views.add_product, name='add_product'),
] 