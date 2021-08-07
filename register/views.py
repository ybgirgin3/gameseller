from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
#from rest_framework.permissions import AllowAny
#from rest_framework.permissions import IsAuthenticated
#from rest_framework.authentication import TokenAuthentication

# for register
@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'yeni hesap başarılı bir şekilde oluşturuldu'
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token

        else:
            data = serializer.errors
        return Response(data)
