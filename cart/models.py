from django.db import models
from decimal import Decimal

# in
#from product.models import Product
from django.contrib.auth.models import User


# sepete ekleme kısmı
class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_owner")
    #product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_item")
    product = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
