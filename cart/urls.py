from django.urls import include, path
from rest_framework import routers, urlpatterns
from . import views

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
router.register(r'carts', views.CartViewSet)
router.register(r'cart_items', views.CartItemViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'order_items', views.OrderItemViewSet),


urlpatterns = router.urls