from django.http import JsonResponse
from .serializers import BasketSerializer, BasketItemSerializer
from django.shortcuts import render, get_object_or_404
from product.models import Product
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import status
#from rest_framework.decorators import detail_route
from rest_framework.decorators import action
#from rest_framework.decorators import list_route
from rest_framework.response import Response
from .basket import Basket, BasketItem
# Create your views here.


class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    
    #@detail_route(methods=['post', 'put'])
    @action(detail=True, methods=['POST', 'PUT'])
    def add_to_basket(self, request, pk=None):
        basket = self.get_object()
        try:
            product = Product.objects.get(
                pk=request.data['product_id']
            )
            quantity = int(request.data['quantity'])
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})

            
        if product.available_inventory <= 0 or product.available_inventory - quantity < 0:
            print("Üründen depoda bulunmamaktadır")
            return Response({'status': 'fail'})

        existing_basket_item = BasketItem.objects.filter(
            basket = basket,
            product = product
        ).first()

        if existing_basket_item:
            existing_basket_item.quantity += quantity
            existing_basket_item.save()
        else:
            new_basket_item = BasketItem(
                basket = basket,
                product = product,
                quantity = quantity
            )
            new_basket_item.save()

        serializer = BasketSerializer(basket)
        return Response(serializer.data)

    #@detail_route(methods=['post', 'put']) 
    @action(detail=True, methods=['POST', 'PUT'])
    def remove_from_basket(self, request, pk=None):
        basket = self.get_object() 
        try:
           product = Product.objects.get(
               pk=request.data['product_id']
           )
        except Exception as e:
           print(e)
           return Response({'status': 'fail'})

        try:
            basket_item = BasketItem.objects.get(
                basket = basket,
                product = product
            )
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})

            
        if basket_item.quantity == 1:
            basket_item.delete()
        else:
            basket_item.quantity -= 1
            basket_item.save()

        serializer = BasketSerializer(basket)
        return Response(serializer.data)

        
class BasketItemViewSet(viewsets.ModelViewSet):
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemSerializer