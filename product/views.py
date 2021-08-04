from django.shortcuts import render
from django.db.models import Q
from django.http import Http404


from rest_framework import filters
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

# Create your views here.
class LatestProductsList(APIView):
     #ana sayfada en son bakılmış olan son 4 elemanı listele
    #renderer_classes = [TemplateHTMLRenderer]
    #template_name = 'product/home.html'

    def get(self, request, format=None):
        product = Product.objects.all()[0:4]
        serializer = ProductSerializer(product, many=True)
        #return Response({'serializer': serializer, 'products': product})
        return Response(serializer.data)

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




