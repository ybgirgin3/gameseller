from django.db import models
from .models import Cart, DeliveryCost
from rest_framework import serializers


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'item', 'quantity', 'created_at', 'updated_at']


class DeliveryCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCost
        fields = ['id', 'status', 'cost_per_delivery', 'cost_per_product', 'fixed_cost', 'created_at', 'update_at']




#class UserSerializer(serializers.Serializer):
#    class Meta:
#        model = User
#        fields = ['id', 'name', 'created_at', 'updated_at']
