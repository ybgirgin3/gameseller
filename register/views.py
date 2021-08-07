from register.models import Account
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import RegistrationSerializer

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

        else:
            data = serializer.errors
        return Response(data)















#class RegisterView(APIView):
#    authentication_classes = [SessionAuthentication, BaseAuthentication]
#    permission_classes = [IsAuthenticated]
#
#    def get(self, request, format=None):
#        content = {
#            'user': str(request.user),
#            'auth': str(request.auth),
#        }
#        return Response(content)




# # for auth
# class MyObtainTokenPairView(TokenObtainPairView):
#     permission_classes = (AllowAny,)
#     serializer_class = MyTokenObtainPairSerializer

