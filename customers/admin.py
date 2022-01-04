"""
    1. Customers address model fields
    2. Append to the user address model fields
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserAddress
# Register your models here.


class AddressAdmin(admin.StackedInline):
    """User address model fields"""
    model = UserAddress
    readonly_fields = ('user',)

    list_display = (
        'user',
        'address_1',
        'address_2',
        'town',
        'county',
        'postcode',
        'country',
    )


class UserAdmin(BaseUserAdmin):
    """Append to base user, user address model fields"""
    inlines = (AddressAdmin,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
