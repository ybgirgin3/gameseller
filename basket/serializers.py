from .basket import Basket, BasketItem
from product.serializers import ProductSerializer
from register.serializers import MyTokenObtainPairSerializer
from rest_framework import serializers


class BasketSerializer(serializers.ModelSerializer):
    customer = MyTokenObtainPairSerializer(read_only=True)
    #items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Basket
        fields = (
            'id', 'customer', 'created_at'#, 'items', 'updated_at'
        )

class BasketItemSerializer(serializers.ModelSerializer):
    basket = BasketSerializer()
    product = ProductSerializer()

    class Meta:
        model = BasketItem
        fields = (
            'id', 'basket', 'product', 'quantity'
        )