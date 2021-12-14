"""
Customers app views
    1. A view to the user profile page

"""
from django.db import models
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserAddress
from .forms import EditProfileForm
from .forms import UserAddressForm
from checkout.models import Order


@login_required
def customers(request):
    """A view to return the user profile page"""
    profile = get_object_or_404(UserAddress, user=request.user)

    if profile.orders:
        orders = profile.orders.all()
    else:
        orders = False

    context = {

            'orders': orders,
        }

    return render(request, 'profile/profile.html', context)


@login_required
def user_details(request):
    """A view to return the user profile details
        Update user Address and Profile details
    """
    profile = get_object_or_404(UserAddress, user=request.user)
    profile2 = request.user

    if request.method == 'POST':

        address_form = UserAddressForm(request.POST, instance=profile)
        user_form = EditProfileForm(request.POST, instance=profile2)
        if address_form.is_valid():
            address_form.save()
            user_form.save()
            messages.success(request, 'Profile data updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure form is valid.')
    else:
        address_form = UserAddressForm(instance=profile)
        user_form = EditProfileForm(instance=profile2)
    context = {
        'address_form': address_form,
        'user_form': user_form,
    }
    
    return render(request, 'profile/user_details.html', context)


@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}.'
    ))
    if request.POST:
        order.status = Order.COMPLETED
        order.save()
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
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
