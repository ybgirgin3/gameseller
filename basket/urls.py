from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'baskets', views.BasketViewSet)
router.register(r'basket_items', views.BasketItemViewSet)

urlpatterns = router.urls