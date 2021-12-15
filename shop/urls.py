from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.shop, name='shop'),
    path('details/<item_id>/', views.shop_item, name='shop_item'),
    path('add/', views.add_item, name='add_item'),
    path('edit/<item_id>', views.edit_item, name='edit_item'),
    path('delete/<item_id>', views.delete_item, name='delete_item'),
    path('order/<order_number>', views.order_details, name='order_details'),
    path('orders', views.orders_view, name='orders_view'),
]
