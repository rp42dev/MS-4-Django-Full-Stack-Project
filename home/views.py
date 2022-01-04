"""Index page views"""
from django.shortcuts import render
from shop.models import Product


# Create your views here.
def index(request):
    """
    A view to return the index page
    Get latest 10 added to the store products
    And return to the index render context
    """
    related = Product.objects.all().order_by('-id')[:10:1]
    context = {
        'related': related
    }
    return render(request, 'home/index.html', context)
