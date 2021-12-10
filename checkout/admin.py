from django.contrib import admin
from .models import Order, OrderLine


class OrderLineAdminInline(admin.TabularInline):
    model = OrderLine
    readonly_fields = ('item_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineAdminInline,)

    readonly_fields = ('user', 'order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total')

    fields = ('order_number', 'user', 'full_name', 'email',
              'address_line_1', 'address_line_2', 
              'town','postcode', 'county', 'country', 'date',
              'delivery_cost','order_total', 'grand_total', 
              'status')

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total', 'status')

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)