"""Support app's url's"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.support, name='support'),
    path('contact', views.contact_view, name='contact_view'),
    path('message/<issue_id>', views.messages_view, name='messages_view'),
    path('submit/<order_number>/', views.submit, name='submit'),
]
