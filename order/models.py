from django.db import models

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(
        #settings.AUTH_USER_MODEL,
    )