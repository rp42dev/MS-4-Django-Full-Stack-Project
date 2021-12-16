from decimal import Decimal
from django.shortcuts import get_object_or_404
from shop.models import Product

def cart_contents(request):
    cart_items = []
    total = 0
    before = 0
    item_count = 0
    availability = 0
    cart = request.session.get('cart', {})

    for item_id, quantity in cart.items():
        
        if isinstance(quantity, int):
            product = get_object_or_404(Product, pk=item_id)
            
            if product.sale:
                subtotal = 0
                total += quantity * product.sale_price
                subtotal = quantity * product.sale_price
                before += quantity * product.price
            else:
                subtotal = 0
                total += quantity * product.price
                subtotal = quantity * product.price
            item_count += quantity
            availability = product.item_count - quantity
            cart_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'product': product,
                'subtotal': subtotal,
                'availability': availability
            })

    if total < 50:
        delivery = total * Decimal(10 / 100)
        free_deivery = 50 * total
    else:
        delivery = 0
        free_deivery = 0

    delivery = round(delivery, 2)
    grand_total = delivery + total
    grand_total = round(grand_total, 2)

    context = {
        'cart_items': cart_items,
        'total': total,
        'before': before,
        'item_count': item_count,
        'delivery': delivery,
        'free_deivery': free_deivery,
        'deivery_treshold': 10,
        'grand_total': grand_total,
    }

    return context
