from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=60)
    friendly_name = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=250)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    special_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProductStatus(models.Model):
    item = models.ForeignKey('Product', null=True, blank=True, on_delete=models.SET_NULL)
    item_count = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return self.name
