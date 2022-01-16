"""
Customers app views
    1. A view to the user profile
    2. A view to the user details profile
    3. A view to the order history
    4. A view to the delete user
"""
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from checkout.models import Order
from support.models import CustomerSuport
from .models import UserAddress
from .forms import EditProfileForm
from .forms import UserAddressForm


@login_required
def customers(request):
    """A view to return the user profile page"""
    order_count = None
    all_orders = False

    profile = request.user
    issues = profile.user_support.all().exclude(status='Resolved')
    issues_count = issues.count()

    reviews = request.user.user_review.all()
    if profile.orders:
        if 'all' in request.GET:
            orders = profile.orders.all().order_by('date')
            all_orders = True
        else:
            orders = profile.orders.all().order_by('date')[:10]
            order_count = orders.count()
    else:
        orders = False

    context = {
        'issues_count': issues_count,
        'order_count': order_count,
        'reviews': reviews,
        'all': all_orders,
        'issues': issues,
        'orders': profile.orders.all(),
    }

    return render(request, 'profile/profile.html', context)


@login_required
def user_details(request):
    """A view to return the user profile details
        Update user Address and Profile details
    """
    address = get_object_or_404(UserAddress, user=request.user)
    profile2 = request.user

    if request.method == 'POST':

        address_form = UserAddressForm(request.POST, instance=address)
        user_form = EditProfileForm(request.POST, instance=profile2)
        if address_form.is_valid():
            address_form.save()
            user_form.save()
            messages.success(
                request, 'Profile data updated successfully')
        else:
            messages.error(
                request, 'Update failed. Please ensure form is valid.')
    else:
        address_form = UserAddressForm(instance=address)
        user_form = EditProfileForm(instance=profile2)
    context = {
        'address_form': address_form,
        'user_form': user_form,
    }

    return render(request, 'profile/user_details.html', context)


@login_required
def order_history(request, order_number):
    """
    A view to order history
    """
    order = get_object_or_404(Order, order_number=order_number)
    profile = request.user

    if not profile.is_superuser:
        if not order.user_profile == profile:
            messages.error(request, 'Only order owner can view this page')
            return redirect(reverse('home'))
    admin = False
    status_form = None

    if 'completed' in request.POST:
        order.status = request.POST['completed']
        order.save()
        messages.success(
            request, f'Thanks for confirming\
            the receipt of the order #: {order.id}.')
        return redirect(reverse('order_history', args=[order_number]))

    issues = CustomerSuport.objects.all()

    try:
        issue = issues.get(order=order)
    except CustomerSuport.DoesNotExist:
        issue = None

    order_reviews = profile.user_review.filter(
        order__order_number=order_number)
    order_list = list()

    for i in order_reviews:
        order_list.append(i.product.id)

    template = 'checkout/checkout-success.html'
    context = {
        'status_form': status_form,
        'issue': issue,
        'order_list': order_list,
        'order': order,
        'from_profile': True,
        'admin': admin,
    }

    return render(request, template, context)


@login_required
def user_delete(request):
    """A view to delete user profile
    """
    profile = get_object_or_404(UserAddress, user=request.user)
    profile2 = request.user

    if request.method == 'POST':
        profile.delete()
        profile2.delete()
        messages.success(request, 'Your account was deleted successfuly')
        return redirect(reverse('account_login'))

    return redirect(reverse('account_login'))
