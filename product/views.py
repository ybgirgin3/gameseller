from django.shortcuts import render
from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

# Create your views here.
class LatestProductsList(APIView):
    # ana sayfada en son bakılmış olan son 4 elemanı listele
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'product/home.html'

    def get(self, request, format=None):
        product = Product.objects.all()[0:4]
        serializer = ProductSerializer(product, many=True)
        return Response({'serializer': serializer, 'products': product})

class ProductDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'product/detail.html'

    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response({'serializer': serializer, 'product': product})

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

        
@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(category__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({'products':[]})
