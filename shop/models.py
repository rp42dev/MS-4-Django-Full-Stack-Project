"""
    1. Product categogy model
    2. Product model to store products to database
"""
from django.db import models
from django.db.models import Avg


class Category(models.Model):
    """Product categogy model"""
    name = models.CharField(max_length=60)
    friendly_name = models.CharField(
        max_length=60, null=True, blank=True)

    def __str__(self):
        """return category  name"""
        return str(self.name)

    def get_friendly_name(self):
        """return category friendly name"""
        return self.friendly_name


class Product(models.Model):
    """Product model to store products to database"""
    sku = models.CharField(max_length=60)
    category = models.ForeignKey(
        'Category', null=True, blank=True,
        on_delete=models.SET_NULL)
    style = models.CharField(max_length=60)
    color = models.CharField(max_length=60)
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=250)
    price = models.DecimalField(
        max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=True, blank=True)
    item_count = models.IntegerField(
        blank=False, null=False, default=0)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=True, blank=True)
    rating_counter = models.PositiveSmallIntegerField(default=0)

    def update_rating(self):
        """Agregate rating each time user rates the product"""
        if (self.product_review):
            self.rating_counter = self.product_review.count()
            self.rating = self.product_review.aggregate(
                Avg('rating'))['rating__avg']
        else:
            self.rating_counter = 0
            self.rating = None
        self.save()

    def save(self, *args, **kwargs):
        """create sku string"""
        if not self.sku:
            try:
                num = Product.objects.latest('id').id + 1
            except Product.DoesNotExist:
                num = 1
            sku = f'{self.style[0]}\
                {str(self.category)[0]}{self.color[0]}-{num}'
            self.sku = sku.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)
