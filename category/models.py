from django.db import models
from django.urls import reverse
from django.utils.html import format_html


class Category(models.Model):
    category_name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=80, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name

    def image(self):
        return format_html('<img src="{}" height="50" style="border-radius:50px;"/>'.format(self.cat_image.url))
