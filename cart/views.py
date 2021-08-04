from django.shortcuts import render
from product.models import Product
from .models import Order, OrderProduct, CartItem
from rest_framework import viewsets, generics, views, exceptions, permissions, mixins

# Create your views here.
class OwnCartViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):

    queryset = CartItem.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(owner=user)
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return serializers.CartItemsSerializer
        else:
            return serializer.CartSerializer

class CheckoutCart(views.APIView):
    def update(self, request, *args, **kwargs):
        user = request.user
        return self._checkout(user)

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')