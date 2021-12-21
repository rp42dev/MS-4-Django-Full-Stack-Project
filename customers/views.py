"""
Customers app views
    1. A view to the user profile
    2. A view to the user details profile
    3. A view to the order history
    4. A view to the delete user
"""
from django.db import models
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserAddress
from .forms import EditProfileForm
from .forms import UserAddressForm
from shop.forms import OrderStatusForm
from checkout.models import Order
from support.models import CustomerSuport
from reviews.models import ProductReview


@login_required
def customers(request):
    """A view to return the user profile page"""
    order_count = None
    all_orders = False
    
    profile = request.user
    reviews = request.user.user_review.all()
    if profile.orders:
        if 'all' in request.GET:
            orders = profile.orders.all()
            all_orders = True
        else:
            orders = profile.orders.all()[:10]
            order_count = orders.count()
    else:
        orders = False

    context = {
            'reviews': reviews,
            'order_count': order_count,
            'all': all_orders,
            'orders': orders,
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
        admin = False
        status_form = None
        if not order.user_profile == profile:
            messages.error(request,  'Only order owner can view this page')
            return redirect(reverse('home'))
    else:
        admin = True
        status_form = OrderStatusForm(instance=order)
        if 'status' in request.POST:
            if status_form.is_valid:
                order.status = request.POST['status']
                order.save()
                messages.success(request, f'Order #{order.id} satus updated to {order.status}')
                return redirect(reverse('order_history', args=[order_number]))
            else: 
                messages.error(request, f'Error validating form please ensure form if valid')
                return redirect(reverse('order_history', args=[order_number]))

    if 'completed' in request.POST:
        order.status = request.POST['completed']
        print(order.status, request.POST['completed'])
        order.save()
        messages.success(
            request,  f'Thanks for confirming\
            the receipt of the order #: {order.id}.')           
        return redirect(reverse('order_history', args=[order_number]))

    issues = CustomerSuport.objects.all()
    try:
        issue = issues.get(order=order)
    except CustomerSuport.DoesNotExist:
        issue = None

    order_reviews = profile.user_review.filter(order__order_number=order_number)
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
