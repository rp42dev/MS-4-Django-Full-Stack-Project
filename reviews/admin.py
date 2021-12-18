from django.contrib import admin
from .models import ProductReview

class ProductReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('user_profile', 'product',
                       'rating', 'order_id', 'date')

    fields = ('user_profile', 'product', 'rating',
              'review', 'order_id', 'date')

    list_display = ('user_profile', 'product',
                    'rating', 'order_id', 'date')
    
    ordering = ('-date',)

admin.site.register(ProductReview, ProductReviewAdmin)
