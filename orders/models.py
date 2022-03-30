from django.db import models
from accounts.models import Account
from store.models import Product, Variation


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='کاربر')
    payment_id = models.CharField(max_length=100, verbose_name='آیدی پرداخت')
    payment_method = models.CharField(max_length=100, verbose_name='روش پرداخت')
    amount_paid = models.CharField(max_length=100, verbose_name='قیمت')
    status = models.CharField(max_length=100, verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ پرداخت')

    def __str__(self):
        return self.payment_id

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت'


class Order(models.Model):
    STATUS = (
        ('جدید', 'جدید'),
        ('قبول', 'قبول'),
        ('تکمیل شده', 'تکمیل شده'),
        ('لغو شده', 'لغو شده'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name='کاربر')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='خرید')
    order_number = models.CharField(max_length=20, verbose_name='شماره سفارش')
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    phone = models.CharField(max_length=15, verbose_name='شماره همراه')
    email = models.EmailField(blank=True, null=True, max_length=50, verbose_name='ایمیل')
    address_line_1 = models.CharField(max_length=50, verbose_name='ادرس ')
    country = models.CharField(max_length=50, verbose_name='کشور')
    state = models.CharField(max_length=50, verbose_name='کوچه')
    city = models.CharField(max_length=50, verbose_name='شهر')
    order_note = models.CharField(max_length=100, blank=True, verbose_name='یادداشت')
    order_total = models.FloatField(verbose_name='قیمت کل')
    status = models.CharField(max_length=10, choices=STATUS, default='New', verbose_name='وضعیت')
    ip = models.CharField(blank=True, max_length=20, verbose_name='ادرس ip')
    is_ordered = models.BooleanField(default=False, verbose_name='وضعیت خرید')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'سفارشات'
        verbose_name_plural = 'سفارشات'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سفارش')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='پرداخت')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    variations = models.ManyToManyField(Variation, blank=True, verbose_name='ایتم های انتخاب شده')
    quantity = models.IntegerField(verbose_name='موجودی')
    product_price = models.FloatField(verbose_name='قیمت محصول')
    ordered = models.BooleanField(default=False, verbose_name='وضعیت سفارش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'سفارش محصول'
        verbose_name_plural = 'سفارش محصولات'
