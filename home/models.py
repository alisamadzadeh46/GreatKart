from django.db import models
from django.utils.html import format_html


class Slider(models.Model):
    image = models.ImageField(upload_to='photos/slider', verbose_name='اسلایدر ')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر'

    def img(self):
        return format_html('<img src="{}" height="50" style="border-radius:50px;"/>'.format(self.image.url))
