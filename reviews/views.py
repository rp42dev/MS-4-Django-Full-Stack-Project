"""
    1. A view to page to post a new reviews
    2. A view to return all the reviews page
"""

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from shop.models import Product
from checkout.models import Order
from .models import ProductReview

from .forms import ReviewForm


@login_required
def review_view(request, item_id):
    """
    A view to page to post a new reviews
    Get product from database by id
    Check if order exists in thwe database
    Check if order matches oser profile
    Post a new reviews to the database
    """
    item = get_object_or_404(Product, pk=item_id)
    profile = request.user

    try:
        order_id = request.GET['order_id']
        order = profile.orders.get(order_number=order_id)
    except Order.DoesNotExist:
        return redirect(reverse('order_history', args=[order_id]))

    if not str(item.id) in order.items:
        messages.error(request, 'Wrong order number')
        return redirect(reverse('order_history', args=[order_id]))

    if not order.user_profile == profile:
        messages.error(request, 'Order number did not match')
        return redirect(reverse('home'))

    order_reviews = profile.user_review.filter(order__order_number=order_id)

    feedback_left = False
    rating = 0
    review = ''
    date = ''

    for i_review in order_reviews:
        if item.id == i_review.product.id:
            rating = i_review.rating
            review = i_review.review
            date = i_review.date
            feedback_left = True

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
                order=order,
            )
            rating_post.save()

            messages.success(request, 'Successfuly added rieview')
            return redirect(reverse('order_history', args=[order_id]))

        else:
            messages.error(request, 'Error with form')
            return redirect(reverse('order_history', args=[order_id]))

    form = ReviewForm()
    context = {
        'feedback_left': feedback_left,
        'order_id': request.GET['order_id'],
        'rating': rating,
        'review': review,
        'form': form,
        'item': item,
        'date': date,
    }
    return render(request, 'review/leave-review.html', context)


def all_reviews(request, item_id):
    """
    A view to return all the reviews page
    Get product by id and return all te reviews#
    related to the product to the all reviews page
    """
    item = get_object_or_404(Product, pk=item_id)
    reviews = item.product_review.all()

    context = {
        'item': item,
        'reviews': reviews,
    }
    return render(request, 'review/reviews.html', context)
