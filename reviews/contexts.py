from .models import ProductReview
from checkout.models import Product


def review_context(request):
    review_items = ProductReview.objects.all()

    context = {
        'review_items': review_items,
    }

    return context
