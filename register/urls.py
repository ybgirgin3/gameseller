from django.urls import path
from .views import registration_view
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'register'

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', obtain_auth_token, name="login"),
]