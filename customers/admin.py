from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from django.contrib import admin
from .models import UserAddress
# Register your models here.


class AddressAdmin(admin.StackedInline):
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
    inlines = (AddressAdmin,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
