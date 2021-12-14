"""
Customers models
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from django_countries.fields import CountryField


class UserAddress(models.Model):
    # User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # User Details
    email = models.EmailField(max_length=100, null=True, blank=True)
    # Shipping Address
    full_name = models.CharField(max_length=50, null=True, blank=True)
    address_1 = models.CharField(max_length=100, null=True, blank=True)
    address_2 = models.CharField(max_length=100, null=True, blank=True)
    town = models.CharField(max_length=60, null=True, blank=True)
    county = models.CharField(max_length=60, null=True, blank=True)
    postcode = models.CharField(max_length=30, null=True, blank=True)
    country = CountryField(blank_label='Country', null=True, blank=True)

    def __str__(self):
        return str(self.user.username)


@receiver(post_save, sender=User)
def update_user_address(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserAddress.objects.create(user=instance)
    # Existing users Shipping Address save the profile data
    else:
        try:
            instance.useraddress.save()
        except ObjectDoesNotExist:
            UserAddress.objects.create(user=instance)

