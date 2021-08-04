from decimal import Decimal
from django.db import models
from django.conf import settings
from product.models import Product

class Basket(models.Model):
    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name = 'basket',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class BasketItem(models.Model):
    basket = models.ForeignKey(
        Basket,
        related_name = 'basket_items',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        Product,
        related_name = 'basket_items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __unicode__(self):
        return '%s: %s' % (self.product.name, self.quantity)
