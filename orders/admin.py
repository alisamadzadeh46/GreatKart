from django.contrib import admin

from orders.models import *


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'payment', 'order_number']
    list_filter = ['status', ]
    search_fields = ['first_name', 'last_name', 'payment', 'order_number']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['status', ]
    list_filter = ['status', ]
