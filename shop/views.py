from django.shortcuts import render, get_object_or_404

from .models import Product, Category


# Create your views here.
def shop(request):
    """A view to return the shop page"""
    categories = Category.objects.all()
    if request.GET:
        if 'category' in request.GET:
            cat = request.GET['category']
            if cat == 'sale':
                products = Product.objects.filter(sale=True)
            elif cat == 'hats':
                products = Product.objects.all()
            else:
                products = Product.objects.filter(category__name=cat)
    else:
        products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'shop/shop.html', context)


# Create your views here.
def shop_item(request, item_id):
    """A view to return the shop item detailed page"""
    item = get_object_or_404(Product, pk=item_id)
    related = Product.objects.filter(style=item.style)
    context = {
        'item': item,
        'related': related,
    }
    return render(request, 'shop/shop_item.html', context)
