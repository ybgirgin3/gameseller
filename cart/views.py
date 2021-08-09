from django.shortcuts import render
from django.db.models import FloatField
from django.db.models import F
from django.db.models import Sum

from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import status, authentication, permissions
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from stripe.api_resources import product

from .models import *
from .serializers import *

from register.models import Account as User
from django.conf import settings

# checkout için
import stripe

# Create your views here.

# checkout
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        stripe.api_key = settings.STRIPE_API_KEY
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])
        try:
            charge = stripe.Charge.create(
                amount = int(paid_amount * 100),
                currency='USD',
                description="GameSeller Alışveriş Merkezi",
                source = serializer.validated_data['stripe_token']
            )
            serializer.save(user=request.user, paid_amount=paid_amount)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            



class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by('id')
    serializer_class = CartSerializer

    @action(detail=True, methods=['post', 'put'])
    def add_to_cart(self, request, pk=None):
        cart = self.get_object()
        try:
            product = Product.objects.get(
                pk=request.data['product_id']
            )
            quantity = int(request.data['quantity'])
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})

            
        if product.available_inventory <= 0 or product.available_inventory - quantity < 0:
            print("Satın alınabilir ürün yok")
            return Response({'status': 'fail'})

        existing_cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
        else:
            new_cart_item = CartItem(cart=cart, product=product, quantity=quantity)
            new_cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)


    @action(detail=True, methods=['post', 'put'])
    def remove_from_cart(self, request, pk=None):
        cart = self.get_object()
        try:
            product = Product.objects.get(
                pk=request.data['product_id']
            )
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})

        try:
            cart_item = CartItem.objects.get(cart=cart,product=product)
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})

        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()

        # return the updated cart to indicate success
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cart items to be viewed or edited.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


    def perform_create(self, serializer):
        try:
            purchaser_id = self.request.data['user']
            user = User.objects.get(pk=purchaser_id)
        except:
            raise serializers.ValidationError(
                "Kullanıcı bulunamadı"
            )

        cart = user.cart

        for cart_item in cart.items.all():
            if cart_item.product.available_inventory - cart_item.quantity < 0:
                raise serializers.ValidationError(
                    "Satın alma işlemini tamamlayabilmek için elimizde" + str(cart_item.product.name) + \
                    "isimli ürünün stoğu kalmamıştır. En yakında zamanda stoklar yenilenecektir. Özür Dileriz.."

                )

        # find the order total using the quantity of each cart item and the product's price
        total_aggregated_dict = cart.items.aggregate(total=Sum(F('quantity')*F('product__price'),output_field=FloatField()))

        order_total = round(total_aggregated_dict['total'], 2)
        order = serializer.save(user=user, total=order_total)

        order_items = []
        for cart_item in cart.items.all():
            order_items.append(OrderItem(order=order, product=cart_item.product, quantity=cart_item.quantity))
            # available_inventory should decrement by the appropriate amount
            cart_item.product.available_inventory -= cart_item.quantity
            cart_item.product.save()


        OrderItem.objects.bulk_create(order_items)
        cart.items.clear()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    #@list_route(url_path="order_history/(?P<user_id>[0-9])")
    @action(detail=False, url_path="order_history/(?P<user_id>[0-9])")
    def order_history(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)

        except:
            # no user was found, so order history cannot be retrieved.
            return Response({'status': 'fail'})

        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer