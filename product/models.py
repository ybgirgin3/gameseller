from django.db import models
from django.db.models.fields import CharField
from django.shortcuts import reverse
from django.conf import settings

# Create your models here.
# oyunun adı - yılı - kategorisi

# kategori modeli
class Category(models.Model):
    """
    name: tanımlanacak / tanımlanmış olan kategorinin adı
    slug: url kısmında url için kullanılacak olan argüman
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    #def create_slug(self):
    #    return slugify(self.name, allow_unicode=True)

    def get_absolute_url(self):
        return f"categories/{self.slug}"

        
# ürünlerin modeli
class Product(models.Model):
    """
    category: ürünler modelini kategori modeline bağımlı hale getirdik
    name    : oyunun adı
    year    : oyunun yılı
    """
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    #owner = models.ForeignKey(User, related_name="product_owner", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_inventory = models.PositiveIntegerField(default=0)
    slug = models.SlugField()

    class Meta:
        ordering = ('-category',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/products/{self.category.slug}/{self.slug}/"

    def get_add_to_cart_url(self):
        return reverse('/cart/add-to-cart', kwargs={
            'slug': self.slug
        })
    

class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total



class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CharField(max_length=10)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code
