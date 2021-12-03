from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<item_id>/', views.add_to_cart, name='add_to_cart'),
]
