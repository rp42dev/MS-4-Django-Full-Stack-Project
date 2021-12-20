from django.contrib import admin
from .models import CustomerSuport


class CustomerSuportAdmin(admin.ModelAdmin):
    readonly_fields = ('user_profile', 'issue', 'message',
                       'order_line', 'order', 'date')

    fields = ('status', 'user_profile',  'order',
              'order_line',  'issue', 'message', 'date')

    list_display = ('issue', 'user_profile', 'order', 'order_line',
                     'date', 'status')

    ordering = ('-date',)

admin.site.register(CustomerSuport, CustomerSuportAdmin)
