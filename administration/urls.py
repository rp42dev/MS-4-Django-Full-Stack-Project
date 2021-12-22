from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.admin_view, name='admin_view'),
    path('order/<order_number>/', views.order, name='order'),
]
