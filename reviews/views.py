from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Product
from .models import ProductReview
from .forms import ReviewForm


@login_required
def review_view(request, item_id):
    """
    A view to return the shop item detailed page
    """
    item = get_object_or_404(Product, pk=item_id)
    if 'order_id' in request.GET:

        order_id = int(request.GET['order_id'])
        order = ProductReview.objects.filter(order_id=order_id)

        # Prevent user leave multiple reviews in same shipping
        for i in order:
            if i.order_id and i.product.id:
                messages.warning(request, f'You already have left\
                    a review for { i.product.name } in order #: {order_id}')
                return redirect(reverse('order_history', args=[order_id]))

        if request.POST:
            form = ReviewForm(request.POST)
            if form.is_valid():
                product = item
                rating = int(request.POST['raiting'])
                review = request.POST['review-review']
                rating_post = ProductReview(
                    product=product,
                    rating=rating,
                    review=review,
                    user_profile=request.user,
                    order_id=order_id
                )
                rating_post.save()

                messages.success(request, 'Successfuly added rieview')
                return redirect(reverse('order_history', args=[order_id]))

            else:
                messages.error(request, 'Error with form')
                return redirect(reverse('order_history', args=[order_id]))

    form = ReviewForm()
    context = {
        'form': form,
        'item': item,
        'order_id': order_id,
    }
    return render(request, 'review/review.html', context)
