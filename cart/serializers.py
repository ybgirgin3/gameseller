from product.serializers import ProductSerializer
from .models import Cart, CartItem, Order, OrderItem
from rest_framework import serializers
from django.conf import settings
from register.models import Account

class UserSerializer(serializers.Serializer):
    class Meta:
        #model = settings.AUTH_USER_MODEL
        model = Account
        fields = ('username', 'email', 'password') 

class CartSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only=True)
    items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'created_at', 'updated_at')

class CartItemSerializer(serializers.Serializer):
    cart = CartSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity')

class OrderSerializer(serializers.Serializer):

    user = UserSerializer(read_only=True)
    order_items = serializers.StringRelatedField(many=True)#, required=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'total', 'created_at', 'updated_at', 'order_items')

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        return order

class OrderItemSerializer(serializers.Serializer):
    order = OrderSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'quantity')
    


    
