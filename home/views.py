from django.shortcuts import render

from ads.models import Ads
from home.models import Slider
from store.models import Product


def home(request):
    ads = Ads.objects.all().filter(is_available=True).order_by('created_date')[:5]
    products = Product.objects.all().filter(is_available=True).order_by('created_date')[:5]
    slider = Slider.objects.all()
    context = {
        'products': products,
        'slider': slider,
        'ads': ads,
    }
    return render(request, 'home/index.html', context)
