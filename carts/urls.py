from django.urls import path
from . import views

app_name = 'carts'
urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product>/', views.add_cart, name='add_cart'),
]
