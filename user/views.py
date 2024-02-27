
from logging import raiseExceptions
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from user.models import User, Followers
from user.permissions import UserPermissions
from utils.utils import UserUtils, CommonUtils

# Create your views here.

class RegisterView(generics.CreateAPIView) :
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def post(self, request):
        if self.request.data['avatar']:
            self.request.data['avatar'] = CommonUtils.UploadToCloud(request.data['avatar'], 'user')

#Login View
class LoginView(generics.GenericAPIView) :
    def post(self, request, *args, **kwargs) :
        try :
            username = request.data['email']
            password = request.data['password']
            
            user = authenticate(password = password, username = username)
            
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status = 200)
        
            else:
                return Response({'status': False, 'message': 'Invalid credentials'}, status=400)
        
        except Exception as e:
                return Response({'status': False, 'message': str(e)}, status=400)


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
          

class UserDetailView(generics.RetrieveAPIView) :
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try :
            token = request.header['Authorization'].split(' ')[1]
            token = Token.objects.get(key = token)
            data = self.serializer(token.user).data
            return Response({'status': True, 'message': data}, status = 200)

        except Exception as e :
            return Response({'status': False, 'message': str(e)}, status = 400)

# ArtistSerializer --- to provide list of all artist
class ArtistListView(generics.ListAPIView) :
    serializer_class = ArtistSerializer
    queryset = User.objects.filter(is_artist = True)
    permission_classes = [permissions.IsAuthenticated]
    
    
##### FOllower Releated views ########

class AddFollowerView(generics.CreateAPIView):
    queryset = Followers.objects.all()
    serializer_class = FollowerSerializer
    permission_class = [permissions.IsAuthenticated]
    
    def post(self, request):
        try :
            data = {}
            token = request.headers['Authorization'].split(' ')[1]
            data['user_id'] = UserUtils.getUserFromToken(token).id
            data['artist_id'] = request.data['artist_id']
            
            if Followers.objects.filter(user_id = data['user_id'], artist_id = data['artist_id']).exists() :
                Followers.objects.get(user_id = data['user_id'], artist_id = data['artist_id']).delete()
                return Response({'status' : True, 'message'  : 'Follower deleted successfully'}, status= 200)
            
            serializer = self.serializer_class(data = data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            
            return Response({'status' : True, 'message'  : 'Follower added successfully'}, status= 200)
   
        except Exception as e:
            return Response({'status' : False, 'message'  : str(e)}, status= 400)
    
class ListAllFollowers(generics.ListAPIView):
    serializer_class = FollowerSerializer
    permission_class = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        id = self.kwargs.get('id')
        return Followers.objects.filter(artist_id = id)
                  
    
# SHORT NAMING :
user_register_view = RegisterView.as_view()
user_logout_view = LogoutView.as_view()
user_detail_view = UserDetailView.as_view()
user_login_view = LoginView.as_view()
add_follower_view = AddFollowerView.as_view()
list_followers_view = ListAllFollowers.as_view()
artist_list_view = ArtistListView.as_view()



