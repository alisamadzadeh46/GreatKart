import admin_thumbnails
from django.contrib import admin
from .models import *


@admin_thumbnails.thumbnail('image')
class ProductGalleryInlineAdmin(admin.TabularInline):
    model = ProductGallery
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'stock', 'category', 'modified_date', 'is_available', 'img']
    prepopulated_fields = {'slug': ['product_name']}
    readonly_fields = ['img', ]
    inlines = [ProductGalleryInlineAdmin]
    list_per_page = 10
    search_fields = ['product_name', 'price', 'stock', 'category', 'modified_date', 'is_available', 'img']
    list_filter = ['stock', 'category', 'is_available']


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_active', 'created_date']
    list_filter = ['is_active', ]
    list_per_page = 10


@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'subject', 'review', 'status']
    search_fields = ['product', 'user', 'subject', 'review', 'status']
    list_per_page = 10


@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ['product', 'img']
    readonly_fields = ['img', ]
    list_per_page = 10
