from decimal import Decimal
from django.shortcuts import get_object_or_404
from shop.models import Product

def cart_contents(request):
    cart_items = []
    total = 0
    item_count = 0
    cart = request.session.get('cart', {})

    for item_id, item_data in cart.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            item_count += item_data
            cart_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })

    if total < 50:
        delivery = total * Decimal(10 / 100)
        free_deivery_delta = 50 * total
    else:
        delivery = 0
        free_deivery_delta = 0

    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'item_count': item_count,
        'delivery': delivery,
        'free_deivery_delta': free_deivery_delta,
        'free_deivery_treshold': 10,
        'grand_total': grand_total,
    }

    return context