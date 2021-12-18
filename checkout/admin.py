from django.contrib import admin
from .models import Order, OrderLine


class OrderLineAdminInline(admin.TabularInline):
    model = OrderLine


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineAdminInline,)

    readonly_fields = ('user_profile', 'order_number', 'date', 'items')

    fields = ('order_number', 'user_profile', 'email', 'shipping_name',
              'shipping_address_1', 'shipping_address_2', 
              'shipping_town', 'shipping_county', 'shipping_postcode', 
              'shipping_country', 'date', 'items', 'delivery',
              'total', 'status')

    list_display = ('order_number', 'date', 'shipping_name',
                    'total', 'delivery', 'status')

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)