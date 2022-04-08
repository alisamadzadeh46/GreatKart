from django.urls import path
from . import views

app_name = 'ad'

urlpatterns = [
    path('', views.ads, name='ads'),
    path('ads_detail/<slug:ads_slug>/', views.ads_detail, name='ads_detail'),
]
