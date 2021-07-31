from django.db import models
from django.urls import reverse

from category.models import Category
from django.utils.html import format_html


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('store:product_detail', args=[self.category.slug, self.slug])

    def img(self):
        return format_html('<img src="{}" height="50" style="border-radius:50px;"/>'.format(self.image.url))
