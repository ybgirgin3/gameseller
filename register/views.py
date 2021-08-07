from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token

# from .serializers import MyTokenObtainPairSerializer

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




# for auth
# class MyObtainTokenPairView(TokenObtainPairView):
#     permission_classes = (AllowAny,)
#     serializer_class = MyTokenObtainPairSerializer

