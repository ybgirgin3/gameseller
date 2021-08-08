from django.db.models import query
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Cart, DeliveryCost
from .serializers import CartSerializer, DeliveryCostSerializer
# from .helpers import CartHelper
#from django.contrib.auth.models import User
from django.conf import settings

# Create your views here.
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by('id')
    serializer_class = CartSerializer

    @action(methods=['get'], detail=False, url_path='checkout/(?P<userId>[^/.]+)', url_name='checkout')
    def checkout(self, request, *args, **kwargs):
        try:
            #user = User.objects.get(pk=int(kwargs.get('userId')))
            user = settings.AUTH_USER_MODEL.objects.get(pk=int(kwargs.get('userId')))
        except Exception as e:
            return Response(status = status.HTTP_404_NOT_FOUND, data={'Error': str(e)})

        # cart_helper = CartHelper(user)
        # checkout_details = cart_helper.prepare_cart_for_checkout()

        # if not checkout_details:
        #     return Response(status = status.HTTP_404_NOT_FOUND, data={'error': 'kullanıcının sepeti boş'})

        
class DeliveryCostViewSet(viewsets.ModelViewSet):
    queryset = DeliveryCost.objects.all()
    serializer_class = DeliveryCostSerializer

    def get(self, request):
        serializer = self.serializer_class(self.queryset)
        return Response(serializer.data)
