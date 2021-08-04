from django import urls
from cart import views
from rest_framework.routers import DefaultRouter
from .views import CartViewSet

router = DefaultRouter()
router.register(r'cart', CartViewSet)


urlpatterns = router.urls