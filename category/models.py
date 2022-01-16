from django.db import models
from django.utils.html import format_html


class Category(models.Model):
    category_name = models.CharField(max_length=80, unique=True, verbose_name='نام دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='دسته بندی')
    description = models.TextField(max_length=80, blank=True, verbose_name='توضیحات')
    cat_image = models.ImageField(upload_to='photos/categories', blank=True, verbose_name='تصویر')

    class Meta:
        verbose_name = 'دسته بندی ها'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.category_name

    def image(self):
        return format_html('<img src="{}" height="50" style="border-radius:50px;"/>'.format(self.cat_image.url))
