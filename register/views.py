from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from serializers import UserSerializer

# Create your views here.
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


class UserSerializerView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


#class UserViewSet(viewsets.ModelViewSet):
#    queryset = User
#    serializer_class = UserSerializer


