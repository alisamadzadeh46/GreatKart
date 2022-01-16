from django.contrib import admin
from .models import *


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'date_added']
    list_filter = ['cart_id', 'date_added']
    list_per_page = 10


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'quantity', 'is_active']
    list_filter = ['quantity', 'is_active']
    list_per_page = 10
