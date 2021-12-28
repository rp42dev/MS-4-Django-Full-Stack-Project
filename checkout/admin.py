from django.contrib import admin
from .models import Order, OrderLine


class OrderLineAdminInline(admin.TabularInline):
    model = OrderLine


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineAdminInline,)

    readonly_fields = ('user_profile', 'order_number', 'date', 'items')

    fields = ('order_number', 'user_profile', 'email', 'shipping_name',
              'address_line_1', 'address_line_2', 
              'town', 'county', 'postcode', 
              'country', 'date', 'items', 'delivery',
              'total', 'status')

    list_display = ('id', 'date', 'shipping_name',
                    'total', 'delivery', 'status')

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)
