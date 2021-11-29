from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.shop, name='shop'),
    path('shop_item/', views.shop_item, name='shop_item'),
]

