import admin_thumbnails
from django.contrib import admin

from ads.models import AdsGallery, Ads


@admin_thumbnails.thumbnail('image')
class AdsGalleryInlineAdmin(admin.TabularInline):
    model = AdsGallery
    extra = 1


@admin.register(Ads)
class AdsAdmin(admin.ModelAdmin):
    list_display = ['ads_name', 'modified_date', 'is_available', 'img']
    prepopulated_fields = {'slug': ['ads_name']}
    readonly_fields = ['img', ]
    inlines = [AdsGalleryInlineAdmin]
    list_per_page = 10
    search_fields = ['ads_name', 'modified_date', 'is_available', ]
    list_filter = ['is_available']
