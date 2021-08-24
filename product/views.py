from django.core.checks import messages
from django.db.models.expressions import RawSQL
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.http import Http404
from rest_framework import filters
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
#from rest_framework.renderers import TemplateHTMLRenderer
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer  # , CartSerializer
from .models import Product

# from django.contrib.auth.decorators import login_required
# from cart.cart import Cart

# Create your views here.

from rest_framework.decorators import api_view
@api_view(['GET'])
def ProductURLPattern(requests):
    api_urls = {
        'ürün listesi': '/products',
        'kategori listesi': '/categories',
        'kategori detayları': '/products/<slug:category_slug>',
        'ürün detayları': '/products/<slug:category_slug>/<slug:product_slug>/',
        'sepet': '/carts/',
        'sepetteki ürünler': '/cart_items',
        'checkout': '/checkout/',
        'siparişi verilmiş ürünlerin listesi': '/order_items',


    }
    return Response(api_urls)

#router.register(r'carts', views.CartViewSet)
#router.register(r'cart_items', views.CartItemViewSet)
#router.register(r'orders', views.OrderViewSet)
#router.register(r'order_items', views.OrderItemViewSet)


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
        # return Response({'serializer': serializer, 'product': product})
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


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


# @api_view(['GET', 'POST'])
# @login_required(login_url="login/")
# def cart_add(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.add(product=product)
#     # return redirect("home")
#     return Response(serilzer)


# @api_view(['GET', 'POST'])
# @login_required(login_url="login/")
# def item_clear(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.remove(product)
#     return redirect("cart_detail")


# @api_view(['GET', 'POST'])
# @login_required(login_url="login/")
# def item_increment(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.add(product=product)
#     return redirect("cart_detail")


# @api_view(['GET', 'POST'])
# @login_required(login_url="login/")
# def item_decrement(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.decrement(product=product)
#     return redirect("cart_detail")


# @api_view(['GET', 'POST'])
# @login_required(login_url="login/")
# def cart_clear(request):
#     cart = Cart(request)
#     cart.clear()
#     return redirect("cart_detail")


# @api_view(['GET', 'POST'])
# @login_required(login_url="login/")
# def cart_detail(request):
#     return render(request, 'cart/cart_detail.html')
