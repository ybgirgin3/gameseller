from django.urls import path
from register.views import UserSerializerView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', UserSerializerView.as_view(), name='token_obtain_pair')
    path('login/refresh/', TokenRefreshView.as_view(), name="token_refresh")
]