"""
    1. Admin product model fields
    2. Admin product category model fields
"""
from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    """Admin product model fields"""
    readonly_fields = ('sku', 'rating', 'rating_counter')
    list_display = (
        'sku',
        'name',
        'category',
        'style',
        'color',
        'price',
        'sale',
        'sale_price',
        'item_count',
    )


class CategoryAdmin(admin.ModelAdmin):
    """Admin product category model fields"""
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
