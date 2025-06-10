from django import forms
from catalog.models import Category, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'image_url', 'description', 'price',
            'available', 'external_url', 'codigo_produto', 'loja', 'pix', 'parcelado'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'https://exemplo.com/imagem.jpg'}),
            'external_url': forms.URLInput(attrs={'placeholder': 'https://exemplo.com/produto'}),
        }
        labels = {
            'codigo_produto': 'Código do Produto',
            'loja': 'Loja',
            'pix': 'Aceita PIX',
            'parcelado': 'Parcelamento disponível',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'order']  # O slug será gerado automaticamente
        labels = {
            'name': 'Nome da Categoria',
            'order': 'Ordem de Exibição',
        }
        widgets = {
            'order': forms.NumberInput(attrs={'min': 0}),
        }