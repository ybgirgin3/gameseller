from rest_framework import serializers, routers, viewsets
from rest_framework_simplejwt.serialzers import TokenObtainPairSerializer
from django.contrib.auth.models import User


#class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super(UserSerializer, cls).get_token(user)

        token['username'] = user.username
        return token



