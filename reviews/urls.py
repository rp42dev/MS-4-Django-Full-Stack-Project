from django.urls import path, include
from . import views


urlpatterns = [
    path('<int:item_id>', views.review_view, name='review_view'),
]
