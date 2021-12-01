from django.shortcuts import render, get_object_or_404

from .models import Product, Category


# Create your views here.
def shop(request):
    """A view to return the shop page"""
    products = Product.objects.all()
    categories = Category.objects.all()
    sortkey = None
    cat = 'hats'
    shop = True

    if request.GET:
        if 'category' in request.GET:
            cat = request.GET['category']
            if cat == 'sale':
                products = Product.objects.filter(sale=True)
            elif cat == 'hats':
                products = Product.objects.all()
            else:
                products = Product.objects.filter(category__name=cat)
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            if sortkey == 'name_asc':
                products = products.order_by('name')
            elif sortkey == 'name_desc':
                products = products.order_by('-name')
            elif sortkey == 'price_asc':
                products = products.order_by('price')
            elif sortkey == 'price_desc':
                products = products.order_by('-price')
    context = {
        'categories': categories,
        'products': products,
        'current_cat': cat,
        'shop': shop,
        'sortkey': sortkey,
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
