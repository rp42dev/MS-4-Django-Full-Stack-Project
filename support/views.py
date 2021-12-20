from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from checkout.models import Order, OrderLine
from .models import CustomerSuport
from .forms import SupportForm
from django.contrib import messages



@login_required
def support(request, order_number):
    """
    A view to return the shop suport page
    """
    order = get_object_or_404(Order, order_number=order_number)
    order_line = OrderLine.objects.filter(order__order_number=order_number)
    profile = request.user

    if not order.user_profile == profile:
        messages.error(request, 'Sorry no order could be found')
        return redirect(reverse('order_history', args=[order_number]))

    if request.POST:
        form = SupportForm(request.POST)
        if form.is_valid():
            product = request.POST['product']
            print(product)
            order_line_item = order_line.get(product_id=product)
            support_post = CustomerSuport(
                status='Submitted',
                user_profile=profile,
                issue=request.POST['support-issue'],
                message=request.POST['support-message'],
                order=order,
                order_line=order_line_item,
            )
            support_post.save()
            messages.success(request, 'Successfuly added rieview')
            return redirect(reverse('order_history', args=[order_number]))

        else:
            messages.error(request, 'Error with form')
            return redirect(reverse('order_history', args=[order_number]))

    form = SupportForm()

    context = {
        'form': form,
        'order': order,
        'order_line': order_line,
    }

    return render(request, 'support/support.html', context)
