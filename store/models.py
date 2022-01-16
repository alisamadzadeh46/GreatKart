from django.db import models
from django.urls import reverse

from accounts.models import Account
from category.models import Category
from django.utils.html import format_html
from django.db.models import Avg, Count


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True, verbose_name='نام محصول ')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='محصول')
    description = models.TextField(max_length=500, verbose_name='توضیحات')
    price = models.IntegerField(verbose_name='قیمت')
    image = models.ImageField(upload_to='photos/products', verbose_name='تصویر')
    stock = models.IntegerField(verbose_name='تعداد موجودی')
    is_available = models.BooleanField(default=True, verbose_name='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='وضعیت')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    modified_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def get_url(self):
        return reverse('store:product_detail', args=[self.category.slug, self.slug])

    def img(self):
        return format_html('<img src="{}" height="50" style="border-radius:50px;"/>'.format(self.image.url))


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    variation_category = models.CharField(max_length=100, choices=variation_category_choice, verbose_name='دسته بندی')
    variation_value = models.CharField(max_length=100, verbose_name='مقدار')
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')
    created_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ ایجاد')

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

    class Meta:
        verbose_name = 'تغییرات و مقدار'
        verbose_name_plural = 'تغییرات و مقدار'


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='کاربر')
    subject = models.CharField(max_length=100, blank=True, verbose_name='عنوان')
    review = models.TextField(max_length=500, blank=True, verbose_name='نظر')
    rating = models.FloatField(verbose_name='امتیاز')
    ip = models.CharField(max_length=20, blank=True, verbose_name='ادرس ip')
    status = models.BooleanField(default=True, verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'نظر و امتیاز ها'
        verbose_name_plural = 'نظر و امتیاز ها'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='photos/products', max_length=255, verbose_name='تصویر')

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'گالری تصاویر'
        verbose_name_plural = 'گالری تصاویر'

    def img(self):
        return format_html('<img src="{}" height="50" style="border-radius:50px;"/>'.format(self.image.url))
