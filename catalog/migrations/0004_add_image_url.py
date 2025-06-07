from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0003_promotion'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.URLField(blank=True, help_text='Link direto da imagem do produto (ex: Cloudinary, Imgur, etc)', max_length=500, verbose_name='URL da Imagem'),
        ),
    ] 