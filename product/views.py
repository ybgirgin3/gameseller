from django.core.checks import messages
from django.db.models.expressions import RawSQL
from django.forms.utils import to_current_timezone
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.decorators import login_required
from rest_framework import filters
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
#from rest_framework.renderers import TemplateHTMLRenderer
from .models import OrderProduct, Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .models import OrderProduct
from .models import Product, OrderProduct, Order, Address, Payment, Coupon
from django.utils import timezone

import string
import random


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


# Create your views here.
#class ProductURLPattern(APIView):

from rest_framework.decorators import api_view
@api_view(['GET'])
def ProductURLPattern(requests):
    api_urls = {
            'ürün listesi': '/products',
            'kategori listesi': '/categories',
            'kategori detayları': '/products/<slug:category_slug>',
<<<<<<< HEAD
            'ürün detayları': '/products/<slug:category_slug>/<slug:product_slug>/',
            'sepet': '/cart/',
            'checkout': '/cart/checkout/'
=======
            'ürün detayları': '/products/<slug:category_slug>/<slug:product_slug>/'
>>>>>>> main
            
    }
    return Response(api_urls)

class ProductDetail(APIView):
    #renderer_classes = [TemplateHTMLRenderer]
    #template_name = 'product/detail.html'

    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        #return Response({'serializer': serializer, 'product': product})
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

        
class ProductSearch(generics.ListAPIView):
    permission_class = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^slug']


class CategorySearch(generics.ListAPIView):
    permission_class = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^slug']



@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderProduct.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Bu ürünün sayısı güncellendi")
            return Response(order)
        else:
            order.items.add(order_item)
            messages.info(request, "Ürün sepetinize eklendi")
            return Response(order)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date
        )
        order.items.add(order_item)
        messages.info(request, "ürün sepetinize eklenmiş")
        return Response(order)
