from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'stock', 'category', 'modified_date', 'is_available', 'img']
    prepopulated_fields = {'slug': ['product_name']}
    readonly_fields = ['img', ]
    list_filter = ['stock', 'category', 'is_available']
