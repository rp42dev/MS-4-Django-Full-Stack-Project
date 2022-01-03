"""Return reviews to context"""
from .models import ProductReview


def review_context(request):
    """Review context returns all the reviews"""

    review_items = ProductReview.objects.all()

    context = {
        'review_items': review_items,
    }

    return context
