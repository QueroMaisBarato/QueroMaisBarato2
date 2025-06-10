from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    order = models.PositiveIntegerField(default=0, help_text='Ordem manual para exibição')
    
    class Meta:
        ordering = ('order', 'name')
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog:home_by_category', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image_url = models.URLField('URL da Imagem', max_length=500, blank=True, help_text='Link direto da imagem do produto (ex: Cloudinary, Imgur, etc)')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    external_url = models.URLField(max_length=500, blank=True, help_text="Link para a plataforma de venda")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    codigo_produto = models.CharField("Código do Produto", max_length=100, blank=True, null=True)
    loja = models.CharField("Loja", max_length=100, blank=True, null=True)
    pix = models.BooleanField("Aceita Pix", default=False, help_text="Marque se o produto pode ser pago via Pix")
    parcelado = models.BooleanField("Parcelado", default=False, help_text="Marque se o produto pode ser parcelado")
    
    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Promotion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='promotions/%Y/%m/%d', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name='promotions')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Promoção'
        verbose_name_plural = 'Promoções'

    def __str__(self):
        return self.title


