"""
Admin Management views
    1. Administrator management view. Requeres login
Post Checkut
    2. Oorder history view and updateorder status
"""
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from shop.forms import OrderStatusForm
from shop.models import Product
from support.models import CustomerSuport
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

    all_orders = Order.objects.all().exclude(
        status='Completed')

    orders = all_orders.exclude(
        status='Submitted').order_by('id')

    new_orders = all_orders.filter(
        status='Submitted').order_by('id')

    new_orders_count = new_orders.count()
    out_of_stock_count = out_of_stock.count()
    low_stock_count = low_stock.count()
    sale_count = sale.count()
    orders_count = orders.count()

    issues = CustomerSuport.objects.all().exclude(
        status='Resolved').order_by('id')
    issues_count = issues.count()
    context = {
        'out_of_stock_count': out_of_stock_count,
        'new_orders_count': new_orders_count,
        'low_stock_count': low_stock_count,
        'out_of_stock': out_of_stock,
        'orders_count': orders_count,
        'issues_count': issues_count,
        'sale_count': sale_count,
        'new_orders': new_orders,
        'low_stock': low_stock,
        'orders': orders,
        'issues': issues,
        'Manage': True,
        'sale': sale,
    }
    return render(request, 'admin/admin.html', context)


@login_required
def order_view(request, order_number):
    """
    A view to order history view
    Get order from database and
    Update order status shipping etc..
    """
    order = get_object_or_404(Order, order_number=order_number)
    user = request.user

    if not user.is_superuser:
        messages.error(request, 'Only administartor can view this page')
        return redirect(reverse('home'))

    profile = order.user_profile
    admin = True
    status_form = OrderStatusForm(
        instance=order, data=request.POST or None)
    if 'status' in request.POST:
        if status_form.is_valid():
            order.status = request.POST['status']
            order.save()
            messages.success(
                request, f'Order #{order.id} satus updated to {order.status}')
            return redirect(reverse('order_view', args=[order_number]))
        else:
            messages.error(
                request, 'Error validating form please ensure form if valid')
            return redirect(reverse('order_view', args=[order_number]))

    issues = CustomerSuport.objects.all()
    try:
        issue = issues.get(order=order)
    except CustomerSuport.DoesNotExist:
        issue = None

    if profile:
        order_reviews = profile.user_review.filter(
            order__order_number=order_number)

        order_list = list()

        for i in order_reviews:
            order_list.append(i.product.id)
    else:
        order_list = None

    template = 'checkout/checkout-success.html'
    context = {
        'status_form': status_form,
        'order_list': order_list,
        'from_profile': False,
        'issue': issue,
        'order': order,
        'admin': admin,
    }

    return render(request, template, context)
