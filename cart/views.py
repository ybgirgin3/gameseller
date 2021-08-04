from django.shortcuts import render
from .models import Cart
from rest_framework import viewsets
from .serializers import CartSerializer

# Create your views here.
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by('-id')
    serializer_class = CartSerializer

    def get(self):
        user = self.request.user
        queryset = self.queryset.filter(owner=user)
        return queryset
        
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)