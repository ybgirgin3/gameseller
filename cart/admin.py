from django.contrib import admin
from .models import Cart, DeliveryCost

# Register your models here.
admin.site.register(Cart)
admin.site.register(DeliveryCost)