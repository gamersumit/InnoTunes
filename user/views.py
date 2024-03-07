from django.utils import timezone
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from music.serializers import SongSerializer
from .serializers import *
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from django.contrib.auth import authenticate
from user.models import User
from utils.utils import CommonUtils, Mail
from comment.models import SongLikes, AlbumLikes, PlaylistLikes
from django.core.mail import send_mail
# Create your views here.

class RegisterView(generics.CreateAPIView) :
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        try :
            urls = []
            CommonUtils.Update_Create(request, ['avatar'], urls)    
            return CommonUtils.Serialize(request.data, UserSerializer)
            
        except Exception as e:
            CommonUtils.delete_media_from_cloudinary(urls)
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
                user.is_deleted = False
                user.save()
                token, created = Token.objects.get_or_create(user=user)
                data = UserSerializer(user).data
                liked_songs = {song.song_id.id : 'id' for song in SongLikes.objects.filter(user_id = user.id)} 
                liked_album = {album.album_id.id : 'id' for album in AlbumLikes.objects.filter(user_id = user.id)} 
                liked_playlist = {playlist.playlist_id.id : 'id' for playlist in PlaylistLikes.objects.filter(user_id = user.id)} 
                user.is_active = True
                user.save()
                return Response({'token': token.key, 'user_info' : data, 'liked_songs' : liked_songs, 'liked_album' : liked_album, 'liked_playlist' : liked_playlist}, status = 200)
        
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
                if not user.is_deleted :
                    user.is_deleted = True
                    user.last_deactivation = timezone.now()
                    user.save()
                    return Response({'message': 'User is inactive and will deleted after 30 days'}, status = 200)
                return Response({'message': 'User is already inactive'}, status = 400)
            else:
                return Response({'status': False, 'message': 'Invalid credentials'}, status=400)
        
        except Exception as e:
                return Response({'status': False, 'message': str(e)}, status=400)   

class UserDetailView(generics.RetrieveAPIView) :
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


# ArtistSerializer --- to provide list of all artist
class UserListView(generics.ListAPIView) :
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username', None)
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset
    
        
class CurrentUserDetailView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]  
    
    def get(self, request):
        try:
            user = UserUtils.getUserFromToken(request.headers['Authorization'].split(" ")[1])
            serializer = self.serializer_class(user)
            return Response(serializer.data, status = 200)
        
        except Exception as e:
            return Response({'message' : str(e)}, status = 400)
        
        
class ArtistListView(generics.ListAPIView) :
    serializer_class = ArtistSerializer
    queryset = User.objects.filter(is_artist = True)
    permission_classes = [permissions.IsAuthenticated]

class ArtistDetailView(generics.RetrieveAPIView):   
    serializer_class = ArtistSerializer
    queryset = User.objects.filter(is_artist = True)
    permission_classes = [permissions.IsAuthenticated]
   


class SendPasswordResetOTPView(generics.UpdateAPIView):
    serializer_class = MailOTPSerializer
    queryset = MailOTP.objects.all()
    
    def put(self, request):
        try:
            subject = 'Passwrod Reset Verfication Mail'
            body = CommonUtils.otp_generator()
            email = request.data['email']
            mail = Mail(subject,f'OTP: {str(body)}', [email])
            
            if User.objects.filter(email = email).exists():
                user = User.objects.get(email = email)
                
                if MailOTP.objects.filter(user_id = user.id).exists():
                    serializer = MailOTP.objects.get(user_id = user.id)
                    serializer.otp = body
                    
                else :
                    data = {'otp' : body, 'user_id' : user.id}
                    serializer = self.serializer_class(data = data)
                    serializer.is_valid(raise_exception=True)
                
                mail.send()
                serializer.save()
            
                return Response({'message' : 'mail sent succesfully'}, status=200)
            
            else :
                raise Exception('EMAIL NOT FOUND')
            
        except Exception as e:
            print(str(e))
            return Response({'message' : str(e)}, status = 400)
    

class resetPasswordTokenGenerationView(APIView):
    http_method_names = ['post']
    def post(self, request):
        try :
            otp = request.data['otp']
            email = request.data['email']
            if User.objects.filter(email = email).exists():
                user = User.objects.get(email = email)
            else : raise Exception('email not found')
            
            if MailOTP.objects.filter(user_id = user.id).exists():
                obj = MailOTP.objects.get(user_id = user.id)
            else : raise Exception('try resending otp')
            
            five_minutes_ago = timezone.now() - timezone.timedelta(minutes=5)
            if obj.updated_at < five_minutes_ago:
                raise Exception('otp expired')
            
            if obj.otp != int(otp):
                raise Exception('incorrect otp')
            
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token' : str(token)}, status = 200)
        
        except Exception as e:
            return Response({'message': str(e)}, status = 400)
        
class resetPasswordView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request):
        try :
            print(request.headers['Authorization'].split(" ")[1])
            user = UserUtils.getUserFromToken(request.headers['Authorization'].split(" ")[1])
            print(user)
            data = {'password' : request.data['password']}
            serializer = self.serializer_class(user, data = data, partial = True)
            print(user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        
            return Response({'message' : 'password reset successfully'}, status = 200)
        except Exception as e:
            return Response({'message': str(e)}, status = 400)
        
# SHORT NAMING :
user_register_view = RegisterView.as_view()
user_logout_view = LogoutView.as_view()
user_detail_view = UserDetailView.as_view()
current_user_detail_view = CurrentUserDetailView.as_view()
user_list_view = UserListView.as_view()
user_login_view = LoginView.as_view()
artist_list_view = ArtistListView.as_view()
artist_detail_view = ArtistDetailView.as_view()
send_otp_password_reset_view = SendPasswordResetOTPView.as_view()
reset_password_token_generation_view = resetPasswordTokenGenerationView.as_view()
reset_password = resetPasswordView.as_view()


