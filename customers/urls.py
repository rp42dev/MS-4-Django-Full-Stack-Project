from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.customers, name='user'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
]
