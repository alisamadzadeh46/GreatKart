from django.db import models

from accounts.models import Account
from store.models import *


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True, verbose_name='ایدی سبد خرید')
    date_added = models.DateField(auto_now_add=True, verbose_name='تاریخ اضافه شدن به سبد خرید')

    def __str__(self):
        return self.cart_id

    class Meta:
        verbose_name = 'اطلاعات سبد خرید'
        verbose_name_plural = 'اطلاعات سبد خرید'


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    variations = models.ManyToManyField(Variation, blank=True, verbose_name='انتخاب شده')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, verbose_name='سبد خرید')
    quantity = models.IntegerField(verbose_name='موجودی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد خرید'
