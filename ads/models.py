from django.db import models
from django.urls import reverse
from django.utils.html import format_html


class Ads(models.Model):
    ads_name = models.CharField(max_length=200, unique=True, verbose_name='نام اگهی ')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='اگهی')
    description = models.TextField(max_length=500, verbose_name='توضیحات')
    image = models.ImageField(upload_to='photos/ads', verbose_name='تصویر')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    modified_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ بروزرسانی')
    is_available = models.BooleanField(default=True, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'تبلیغ'
        verbose_name_plural = 'تبلیغات'

    def __str__(self):
        return self.ads_name

    # def averageReview(self):
    #     reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
    #     avg = 0
    #     if reviews['average'] is not None:
    #         avg = float(reviews['average'])
    #     return avg
    #
    # def countReview(self):
    #     reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
    #     count = 0
    #     if reviews['count'] is not None:
    #         count = int(reviews['count'])
    #     return count

    def img(self):
        return format_html('<img src="{}" height="50" style="border-radius:50px;"/>'.format(self.image.url))


class AdsGallery(models.Model):
    ads = models.ForeignKey(Ads, default=None, on_delete=models.CASCADE, verbose_name='اگهی')
    image = models.ImageField(upload_to='photos/ads', max_length=255, verbose_name='تصویر')

    def __str__(self):
        return self.ads.ads_name

    class Meta:
        verbose_name = 'گالری تصاویر اگهی'
        verbose_name_plural = 'گالری تصاویر اگهی'

    def img(self):
        return format_html('<img src="{}" height="50" style="border-radius:50px;"/>'.format(self.image.url))
