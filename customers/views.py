"""
Customers app views
    1. A view to the user profile page

"""
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def customers(request):
    """A view to return the user profile page"""
    profile = models.OneToOneField(User, on_delete=models.CASCADE)
    user = User.objects.all()
    context = {
        'profile': profile,
        'user': user,
    }
    return render(request, 'profile/profile.html', context)
