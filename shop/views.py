from django.shortcuts import render, get_object_or_404

from .models import Product, Category


# Create your views here.
def shop(request):
    """A view to return the shop page"""
    products = Product.objects.all()
    categories = Category.objects.all()
    style_list = products.values('style').distinct()
    sortkey = None
    sort_name = None
    style = 'select'
    category  = 'all'
    shop = True
    if request.GET:
        if 'category' in request.GET:
            category = request.GET['category']
            if category == 'sale':
                products = products.filter(sale=True)
            elif category == 'all':
                products = products.all()
            else:
                products = products.filter(category__name=category)
        if 'style' in request.GET:
            style = request.GET['style']
            if style != 'select':
                products = products.filter(style=style)
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            if sortkey == 'name_asc':
                sort_name = 'Name (A-Z)'
                products = products.order_by('name')
            elif sortkey == 'name_desc':
                sort_name = 'Name (Z-A)'
                products = products.order_by('-name')
            elif sortkey == 'price_asc':
                sort_name = 'Price (L-H)'
                products = products.order_by('price')
            elif sortkey == 'price_desc':
                sort_name = 'Price (H-L)'
                products = products.order_by('-price')
    context = {
        'categories': categories,
        'products': products,
        'cat': category,
        'sortkey': sortkey,
        'sort_name': sort_name,
        'style_list': style_list,
        'style': style,
        'shop': shop,
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
