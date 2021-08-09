from django.db import models

# user'ı contrib üzerinden değil register app üzerinden alacağız
from django.conf import settings
from product.models import Product

# Create your models here.

# create cart for a user
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user)


# create items for created cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,
                             related_name='items',
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)
    product = models.ForeignKey(Product,
                                related_name='items',
                                on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.cart} - {self.product} - {self.quantity}"

# order model
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='orders',
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user)


# order item model
class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='order_items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.name}: {self.quantity}"
