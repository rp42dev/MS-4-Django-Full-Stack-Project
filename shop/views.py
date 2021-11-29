from django.shortcuts import render, get_object_or_404

from .models import Product, Category


# Create your views here.
def shop(request):
    """A view to return the shop page"""
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'shop/shop.html', context)


# Create your views here.
def shop_item(request, item_id):
    """A view to return the shop item detailed page"""
    item = get_object_or_404(Product, pk=item_id)
    context = {
        'item': item,
    }
    return render(request, 'shop/shop_item.html', context)
