"""Home app's url's"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
]
