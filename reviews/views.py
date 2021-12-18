from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import ProductReview
from shop.models import Product
from .forms import ReviewForm


@login_required
def review_view(request, item_id):
    """
    A view to return the shop item detailed page
    """
    item = get_object_or_404(Product, pk=item_id)
    feedback_left = False
    rating = 0
    review = ''
    date = ''
    if 'order_id' in request.GET:

        order_id = int(request.GET['order_id'])
        order = ProductReview.objects.filter(order_id=order_id)

        # Prevent user leave multiple reviews in same shipping
        for i in order:
            if i.order_id and i.product.id == item_id:
                feedback_left = True
                rating = i.rating
                review = i.review
                date = i.date

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
                    order_id=int(request.POST['order_id'])
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
        'feedback_left': feedback_left,
        'rating': rating,
        'review': review,
        'date': date,
    }
    return render(request, 'review/leave-review.html', context)


def all_reviews(request, item_id):
    """
    A view to return the shop item detailed page
    """
    item = get_object_or_404(Product, pk=item_id)

    reviews = ProductReview.objects.filter(product=item)

    context = {
        'item': item,
        'reviews': reviews,
    }
    return render(request, 'review/reviews.html', context)

