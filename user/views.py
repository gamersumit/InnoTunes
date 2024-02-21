
from rest_framework import generics
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.authtoken.models import Token


# Create your views here.

class RegisterView(generics.CreateAPIView) :
    serializer_class = UserSerializer
    queryset = User.objects.all()


# logout view // delete token       
class LogoutView(generics.RetrieveAPIView) :
    def get(self, request):
        try :
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Token '):
                token = auth_header.split(' ')[1]
                token = Token.objects.get(key = token)
                token.delete()
                return Response({'status': True, 'message': 'User Logout Successfully'}, status = 200)
            
            else :
                return Response({'status': False, 'message': 'Missing Token'}, status = 400)
        
        except Exception as e :
            return Response({'status': False, 'message': str(e)}, status = 400)
            
        
# SHORT NAMING :
user_register_view = RegisterView.as_view()
user_logout_view = LogoutView.as_view()