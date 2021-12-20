from django.urls import path, include
from . import views


urlpatterns = [
    path('<order_number>/', views.support, name='support'),
]
