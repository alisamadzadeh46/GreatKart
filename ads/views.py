from django.shortcuts import render

from ads.models import Ads, AdsGallery
from django.core.paginator import Paginator


def ads_detail(request, ads_slug):
    try:
        single_ads = Ads.objects.get(slug=ads_slug)
    except Exception as e:
        raise e
    ads_gallery = AdsGallery.objects.filter(ads_id=single_ads.id)
    context = {
        'single_ads': single_ads,
        'ads_gallery': ads_gallery,
    }
    return render(request, 'ads/ads-detail.html', context)


def ads(request, ads_slug=None):
    if ads_slug is not None:
        ads = Ads.objects.filter(is_available=True)
        paginator = Paginator(ads, 6)
        page = request.GET.get('page')
        paged_ads = paginator.get_page(page)
        ads_count = ads.count()
    else:
        products = Ads.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_ads = paginator.get_page(page)
        ads_count = products.count()

    context = {
        'ads': paged_ads,
        'ads_count': ads_count,

    }
    return render(request, 'ads/ads.html', context)
