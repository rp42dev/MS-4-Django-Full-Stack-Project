"""Url's for Shop app"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.shop, name='shop'),
    path('details/<item_id>/', views.shop_item, name='shop_item'),
    path('add/', views.add_item, name='add_item'),
    path('edit/<item_id>', views.edit_item, name='edit_item'),
    path('delete/<item_id>', views.delete_item, name='delete_item'),
]
