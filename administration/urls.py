from django.urls import path
from . import views


urlpatterns = [
    path('', views.admin_view, name='admin_view'),
    path('order/<order_number>/', views.order_view, name='order_view'),
]
