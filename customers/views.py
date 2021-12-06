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
from .forms import UserAddressForm
from .forms import EditProfileForm


@login_required
def customers(request):
    """A view to return the user profile page"""
    # user = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        # form = UserProfileForm(request.POST, instance=user)
        user_form = EditProfileForm(request.POST, instance=request.user)
        address_form = UserAddressForm(request.POST, instance=request.user)
        if form.is_valid():
            user_form.save()
            address_form.save()
            messages.success(request, 'Profile data updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure form is valid.')
    else:
        user_form = EditProfileForm(request.POST, instance=request.user)
        address_form = UserAddressForm(request.POST, instance=request.user)
    context = {
        'user_form': user_form,
        'address_form': address_form,
        'user': request.user,
    }

    return render(request, 'profile/profile.html', context)
