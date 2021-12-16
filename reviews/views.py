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
                user_profile=request.user
            )
            rating_post.save()

            messages.success(request, 'Successfuly added rieview')
            return redirect(reverse('shop_item', args=[item.id]))
    form = ReviewForm()
    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'review/review.html', context)
