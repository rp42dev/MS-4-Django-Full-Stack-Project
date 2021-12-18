from django.contrib.auth.models import User
from django.contrib import admin
from .models import UserAddress
# Register your models here.


class AddresstAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)

    list_display = ( 
        'user',
        'email',
        'full_name',
        'address_1',
        'address_2',
        'town',
        'county',
        'postcode',
        'country',
    )

admin.site.register(UserAddress, AddresstAdmin)
