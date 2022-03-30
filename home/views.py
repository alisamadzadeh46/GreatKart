from django.shortcuts import render

from home.models import Slider
from store.models import Product


def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')[:5]
    slider = Slider.objects.all()
    context = {
        'products': products,
        'slider': slider,
    }
    return render(request, 'home/index.html', context)
