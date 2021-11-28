
from django.contrib import admin
from .models import Product, Category, ProductStatus

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'special_price',
        'image',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ProductStatusAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'item_count',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductStatus, ProductStatusAdmin)
