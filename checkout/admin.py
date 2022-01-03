from django.contrib import admin
from .models import Order, OrderLine


class OrderLineAdminInline(admin.TabularInline):
    """Admin Order Line items"""
    model = OrderLine


class OrderAdmin(admin.ModelAdmin):
    """Orders form fields and inlines"""
    inlines = (OrderLineAdminInline,)

    readonly_fields = ('user_profile', 'order_number', 'date', 'items', 'stripe_pid')

    fields = ('order_number', 'user_profile', 'email', 'shipping_name',
              'address_line_1', 'address_line_2',
              'city', 'county', 'postcode',
              'country', 'date', 'items', 'delivery',
              'total', 'status', 'paid', 'stripe_pid')

    list_display = ('id', 'date', 'shipping_name',
                    'total', 'delivery', 'status', 'paid')

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
