from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.customers, name='user'),
    path('details', views.user_details, name='user_details'),
    path('delete', views.user_delete, name='user_delete'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
]
