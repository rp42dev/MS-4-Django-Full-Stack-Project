from django.shortcuts import render


# Create your views here.
def shop(request):
    """A view to return the shop page"""
    return render(request, 'shop/shop.html')


# Create your views here.
def shop_item(request):
    """A view to return the shop item detailed page"""
    return render(request, 'shop/shop_item.html')
