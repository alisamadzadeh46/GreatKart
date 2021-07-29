from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=80, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=80, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    def __str__(self):
        return self.category_name
