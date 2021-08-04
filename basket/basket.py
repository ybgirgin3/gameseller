from decimal import Decimal
from django.db import models
from django.conf import settings
from product.models import Product

# Create your models here.
class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, qty):
        """
        sepete ürün ekleme ve güncelleme fonksiyonu
        """
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price), "qty": qty}

        self.save()

        
    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.object.filter(id__in=product_ids)
        basket = self.basket.copy()

        for prod in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item
            

    def update(self, product, qty):
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty
        self.save()

    def get_total_price(self):
        newprice = 0.00
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

        total = subtotal + Decimal(newprice)
        return total

        
    def delete(self, product):
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

