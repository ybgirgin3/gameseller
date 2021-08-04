from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Cart
        fields = '__all__'
