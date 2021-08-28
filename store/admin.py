from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'stock', 'category', 'modified_date', 'is_available', 'img']
    prepopulated_fields = {'slug': ['product_name']}
    readonly_fields = ['img', ]
    list_filter = ['stock', 'category', 'is_available']


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category', 'variation_value', 'is_active', 'created_date',]
    list_filter = ['is_active', 'variation_category',]