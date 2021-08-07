from rest_framework import serializers
from .models import Account
from django.contrib.auth.models import User
#from rest_framework.validators import UniqueValidator
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = Account(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password not match'})
        account.set_password(password)
        account.save()
        return account









# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

#    @classmethod
#    def get_token(cls, user):
#        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

#        # Add custom claims
#        token['username'] = user.username
#        return token

