"""
Customers app views
    1. A view to the user profile page

"""
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserAddress
from .forms import EditProfileForm
from .forms import UserAddressForm


@login_required
def customers(request):
    """A view to return the user profile page"""
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
    
    return render(request, 'profile/profile.html', context)
