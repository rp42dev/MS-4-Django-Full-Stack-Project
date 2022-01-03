"""Review app Url's"""
from django.urls import path
from . import views


urlpatterns = [
    path('<int:item_id>/', views.review_view, name='review_view'),
    path('all/<int:item_id>/', views.all_reviews, name='all_reviews'),
]
