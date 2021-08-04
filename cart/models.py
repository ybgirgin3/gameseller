from django.db import models
from product.models import Product

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CartItem(BaseModel):
    owner = models.ForeignKey(AbstractUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, blank=False, null=False)

    def __unicode__(self):
        return "%x %s" % (self.quantity, self.product.name)


class Order(BaseModel):
    owner = models.ForeignKey(AbstractUser, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='OrderProduct', through_fields=('order', 'product'))

class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, blank=True, null=True)

    def __unicode__(self):
        return "%x %s" % (self.quantity, self.product.name)

