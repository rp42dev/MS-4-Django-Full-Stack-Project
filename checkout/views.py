from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from shop.models import Product
from customers.models import UserAddress
from . models import Order
from . forms import OrderForm

def checkout(request):
    """
    A view to return the checkout page
    """
    if request.user:
        profile = UserAddress.objects.get(user=request.user)
        # user = User.objects.get(user=request.user)
        form = OrderForm(initial={
            'full_name': f'{request.user.first_name} {request.user.last_name}',
            'email': request.user.email,
            'address_line_1': profile.address_line_1,
            'address_line_2': profile.address_line_2,
            'town': profile.town,
            'postcode': profile.postcode,
            'county': profile.county,
            'country': profile.country,
        })
    else:  
        form = OrderForm()
    context={
        'form': form,
    }
    return render(request, 'checkout/checkout.html', context)
