from django.db import models

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

    def get_absolute_url(self):
        return f"/{self.slug}/"

        
# ürünlerin modeli
class Product(models.Model):
    """
    category: ürünler modelini kategori modeline bağımlı hale getirdik
    name    : oyunun adı
    year    : oyunun yılı
    """
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    year = models.DateTimeField()

    class Meta:
        ordering = ('-year',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.category.slug}/{self.title}/"





