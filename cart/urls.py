"""Url's' for cart app"""

from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<item_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<item_id>/', views.update_cart, name='update_cart'),
    path('delete/<item_id>/', views.remove_cart_item, name='remove_cart_item'),
]
