from django.urls import path
from .views import registration_view, LoginAPIView
#from rest_framework.authtoken.views import obtain_auth_token


app_name = 'register'

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', LoginAPIView.as_view(), name="login"),
]