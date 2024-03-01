
from rest_framework import generics
from rest_framework.response import Response

from music.serializers import SongSerializer
from .serializers import *
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from django.contrib.auth import authenticate
from user.models import User
from utils.utils import CommonUtils
from comment.models import SongLikes

# Create your views here.

class RegisterView(generics.CreateAPIView) :
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        try :
            CommonUtils.Update_Create(request, ['avatar'])
            return CommonUtils.Serialize(request.data, UserSerializer)
            
        except Exception as e:
            return Response({'message' : str(e)}, status = 400)
        
#Login View
class LoginView(generics.GenericAPIView) :
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs) :
        try :
            username = request.data['email']
            password = request.data['password']
            
            if not User.objects.filter(email = username).exists() :
               return Response({'status': False, 'message': 'New User'}, status=400)
                
            user = authenticate(password = password, username = username)
            
            if user:
                token, created = Token.objects.get_or_create(user=user)
                data = UserSerializer(user).data
                liked_songs = [song.song_id for song in SongLikes.objects.filter(user_id = user.id)]
                liked_songs = SongSerializer(liked_songs, many = True).data
                return Response({'token': token.key, 'user_info' : data, 'liked_songs' : liked_songs}, status = 200)
        
            else:
                return Response({'status': False, 'message': 'Invalid credentials'}, status=400)
        
        except Exception as e:
                return Response({'status': False, 'message': str(e)}, status=400)

# logout view // delete token       
class LogoutView(generics.RetrieveAPIView) :
    permission_classes = [permissions.IsAuthenticated]
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
    
    
    def delete(self, request, *args, **kwargs) :
        try :
            username = request.data['email']
            password = request.data['password']
            
            user = authenticate(password = password, username = username)
           
        
            if user:
                user.delete()
                return Response({'message': 'User Deleted Sucessfully'}, status = 200)
        
            else:
                return Response({'status': False, 'message': 'Invalid credentials'}, status=400)
        
        except Exception as e:
                return Response({'status': False, 'message': str(e)}, status=400)   

class UserDetailView(generics.RetrieveAPIView) :
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class UserListView(generics.ListAPIView) :
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

        
# ArtistSerializer --- to provide list of all artist
class ArtistListView(generics.ListAPIView) :
    serializer_class = ArtistSerializer
    queryset = User.objects.filter(is_artist = True)
    permission_classes = [permissions.IsAuthenticated]

class ArtistDetailView(generics.RetrieveAPIView):   
    serializer_class = ArtistSerializer
    queryset = User.objects.filter(is_artist = True)
    permission_classes = [permissions.IsAuthenticated]
   
    
    
# SHORT NAMING :
user_register_view = RegisterView.as_view()
user_logout_view = LogoutView.as_view()
user_detail_view = UserDetailView.as_view()
user_list_view = UserListView.as_view()
user_login_view = LoginView.as_view()
artist_list_view = ArtistListView.as_view()
artist_detail_view = ArtistDetailView.as_view()



