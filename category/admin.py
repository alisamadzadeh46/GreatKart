from django.contrib import admin

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'slug', 'image']
    list_filter = ['category_name', 'slug']
    readonly_fields = ['image', ]
    prepopulated_fields = {'slug': ('category_name',)}
    search_fields = ['category_name', 'slug']
