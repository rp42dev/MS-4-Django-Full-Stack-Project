from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from reviews.models import ProductReview
from shop.models import Product, Category
from support.models import CustomerSuport, Message
from checkout.models import Order



@login_required
def admin_view(request):
    """
    Administrator management view. Requeres login and
    superuser privileges. Returns low stock products,
    Order status items and product discount items
    """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can do that')
        return redirect(reverse('home'))

    products = Product.objects.all()
    low_stock = products.filter(
        item_count__lte=5).exclude(item_count=0)
    out_of_stock = products.filter(item_count=0)
    sale = products.filter(sale=True)

    orders = Order.objects.all().exclude(status='Completed')

    out_of_stock_count = out_of_stock.count()
    low_stock_count = low_stock.count()
    sale_count = sale.count()
    orders_count = orders.count()

    issues = CustomerSuport.objects.all().exclude(status='Resolved')
    issues_count = issues.count()
    print(issues)
    context = {
        'out_of_stock_count': out_of_stock_count,
        'low_stock_count': low_stock_count,
        'out_of_stock': out_of_stock,
        'orders_count': orders_count,
        'issues_count': issues_count,
        'sale_count': sale_count,
        'low_stock': low_stock,
        'orders': orders,
        'issues': issues,
        'Manage': True,
        'sale': sale,
    }
    return render(request, 'admin/admin.html', context)
