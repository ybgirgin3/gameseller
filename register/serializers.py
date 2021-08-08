from rest_framework import serializers
from .models import Account
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _


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

class LoginSerializer(serializers.Serializer):
    model = Account
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label = _("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username = username, password = password)
            if not user:
                msg = _('girilen bilgilere göre giriş yapılamıyor')
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = _('email adı ve parola değerleri boş olmaz')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs





                
