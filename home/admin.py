from django.contrib import admin

from home.models import Slider


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['img', ]
    readonly_fields = ['img', ]
    list_per_page = 10
