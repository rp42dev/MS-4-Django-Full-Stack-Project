from django.shortcuts import render
from shop.models import Product


# Create your views here.
def index(request):
    """A view to return the index page"""
    related = Product.objects.all()
    context = {
        'related': related
    }
    return render(request, 'home/index.html', context)
