from django.contrib.auth.models import User
from django.db import models

from shop.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.cart.user.username + ' - ' + self.product.name

    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзине'
