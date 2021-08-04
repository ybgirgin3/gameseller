from django.contrib.auth import get_user_model
from .models import CartItem, Order, OrderProduct
from product.models import Product
from product.serializers import ProductSerializer
from rest_framework import serializer, exceptions

User = get_user_model()

class CartSerializer(serializer.HyperlinkedModelSerializer):
    class Meta:
        model = CartItem
        fields = ('quantity', 'product')
    product = ProductSerializer()

class CartItemSerializer(serializer.HyperlinkedModelSerializer):
    product_id = serializer.PositiveIntegerField(required=True, write_only=True)
    quantity = serializer.PositiveIntegerField(default=1)
    product = ProductSerializer(read_only=True)

class CartItemsSerializer(serializer.Serializer):
    products = serializers.ListField(child=CartItemSerializer())

    def create(self, validated_data):
        """ sepete ürün ekle """
        user = self.context['request'].user
        current_cart = CartItem.object.filter(owner=user)
        current_cart_items_id = map(lambda item: item.product_id, current_cart)

        cart_items = list()

        for prod_data in validated_data['products']:
            product_id = prod_data['product_id']

            if product_id in current_cart_items_id:
                raise exceptions.ParseError(detail = "Ürün (%s) zaten sepette var" % product_id)
                return
            try:
                product = Product.object.get(id=product_id)
            except Product.DoesNotExist:
                raise exceptions.ParseError(detail = "Böyle bir ürün yok (%s) " % product_id)
                return 

            quantity = prod_data['quantity']
            cart_items.append(
                CartItem(owner=user, product=product, quantity=quantity)
            )
        result = CartItem.objects.bulk_create(cart_items)
        response = {'products': list(current_cart) + result}
        return response


class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('quantity', 'product')

    product = ProductSerializer(many=False, read_only=True)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'created_at', 'url', 'orderproduct_set')

    orderproduct_set = OrderProductSerializer(many=True, read_only=True)