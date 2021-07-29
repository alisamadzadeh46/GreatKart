from django.contrib import admin

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'slug']
    list_filter = ['category_name', 'slug']
    prepopulated_fields = {'slug': ('category_name',)}
    search_fields = ['category_name', 'slug']
