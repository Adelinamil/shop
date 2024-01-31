from django.db import models
from django.urls import reverse


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=110, db_index=True, unique=True, verbose_name='Cтроковое представление в URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:products_by_category', args=[1, self.slug])

    class Meta:
        verbose_name = 'Категория продукта'
        verbose_name_plural = 'Категории продуктов'


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products',
                                 verbose_name='Категория')
    name = models.CharField(max_length=30, verbose_name='Название продукта')
    slug = models.SlugField(max_length=35, unique=True, db_index=True, verbose_name='Cтроковое представление в URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание продукта')
    country = models.CharField(max_length=100, verbose_name='Страна поставщика')
    color = models.CharField(max_length=100, verbose_name='Цвет')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    amount = models.IntegerField(default=0, verbose_name='Количество')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
