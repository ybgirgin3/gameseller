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
   
