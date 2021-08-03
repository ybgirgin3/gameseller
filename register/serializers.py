from rest_framework import serializers, routers, viewsets
from djnago.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']




#from register.models import Register
#class RegistrationSerializer(serializers.ModelSerializer):
#    password2 = serializers.CharField(
#        style={'input_type': 'password'}, write_only=True)
#
#    class Meta:
#        model = Register
#        fields = ['email', 'username', 'password', 'password2']
#        extra_kwargs = {
#            'password': {'write_only': True}
#        }
#
#    def save(self):
#        account = Register(
#            email = self.validated_data['email'],
#            username = self.validated_data['username'],
#        )
#
#        password = self.validated_data['password']
#        password2 = self.validated_data['password2']
#
#        if password != password2:
#            raise serializers.ValidationError(
#                {'password': 'Girilen Sifreler Farkı'}
#            )
#
#        account.set_password(password)
#        account.save()
#        return account

