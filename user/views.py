from functools import partial
from django.utils import timezone
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
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
from django.contrib.auth.views import LogoutView as DRFLogoutView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

class RegisterView(generics.CreateAPIView) :
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(tags = ['Auth'], 
    operation_summary= "REGISTER", operation_description = 'REGISTER YOURSELF TO USE OUR APPLICATION AND APIS', 
    responses={200: openapi.Response('Registeration Successful')},
    )       
    def post(self, request):
        try :
            urls = []
            CommonUtils.Update_Create(request, ['avatar'], urls)    
            response = CommonUtils.Serialize(request.data, UserSerializer)
            if response.status_code == 200 :
                UserUtils.sendMailVerificationLink(email = request.data['email'])
            return response    
        
        except Exception as e:
            CommonUtils.delete_media_from_cloudinary(urls)
            return Response({'message' : str(e)}, status = 400)

class ResendEmailVerificationLink(generics.CreateAPIView):
    # serializer_class = None
    queryset = User.objects.all()

    @swagger_auto_schema(tags = ['Auth'], 
    operation_summary= "SEND VERIFICATION LINK", operation_description = 'RESEND ACCOUNT VERIFICATION LINK', 
    responses={200: 'Link Sent to Registered email.'},
    request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    ) 
    def post(self, request):
        try : 
            email = request.data['email']

            user = User.objects.filter(email = email).first() 
           
            if not user:    
                raise Exception('Invalid Email ID')
            
            if user.is_verified:
                raise Exception('User Already Verified')

            UserUtils.sendMailVerificationLink(email = email)
            return Response({'message' : 'Link Sent to Registered email.'}, status=200)
        
        except Exception as e:
            return Response({'message' : str(e)}, status=400)
class UpdateUserProfileView(generics.GenericAPIView) :
    serializer_class = UserProfileUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
    tags = ['User'],
    operation_summary= "EDIT PROFILE", operation_description = '', 
    responses={200: openapi.Response('Profile Updated Succesfully', UserProfileUpdateSerializer)},
    
    ) 
    def put(self, request):
        try :
            urls = []

            user = UserUtils.getUserFromToken(request.headers['Authorization'].split(' ')[1])
            current_avatar = None    
            if request.data.get('avatar', None):
                CommonUtils.Update_Create(request, ['avatar'], urls) 
                current_avatar =  user.avatar 
                        
            serializer = UserProfileUpdateSerializer(user, request.data, partial = True)  
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            if current_avatar:
                CommonUtils.delete_media_from_cloudinary([current_avatar])
            

            return Response({'message' : 'Profile Updated Succesfully', 'data' : serializer.data}, status = 200)
            
        except Exception as e:
            CommonUtils.delete_media_from_cloudinary(urls)
            return Response({'message' : str(e)}, status = 400)
        
#Login View
class LoginView(generics.GenericAPIView) :
    serializer_class = LoginSerializer

    @swagger_auto_schema(tags = ['Auth'], 
    operation_summary= "LOGIN", operation_description = 'GET LOGIN TOKEN AND USER DASHBOARD DETAILS ON LOGIN VIA EMAIL & PASSWORD', 
    responses={200: openapi.Response('Login Successful', LoginResponseSerializer)})       
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
                
                if not user.is_verified:
                    return Response({'status': False, 'message': 'Please verify your email first'}, status=403)
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

    @swagger_auto_schema(tags = ['Auth'], 
    operation_summary= "LOGOUT", operation_description = 'Token Deletion', 
    responses={200: openapi.Response('User Logout Successfully')})       
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
    
    
    @swagger_auto_schema(tags = ['Auth'], 
    operation_summary= "DELETE ACCOUNT", operation_description = 'Account will not be deleted immediately but will be marked as inactive and an inactive account will be deleted automatically after 30 DAYS if not activated again', 
    responses={200: openapi.Response('Account is inactive and will be deleted after 30 days')})  
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
                    return Response({'message': 'Account is inactive and will be deleted after 30 days'}, status = 200)
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

    @swagger_auto_schema(
    tags = ['User'],
    operation_summary= "USER DETAILS WITH USER ID", operation_description = 'Provides User\'s details expecting User Id IN URL', 
    responses={200: openapi.Response('', UserSerializer)})       
    def get(self, request, id):
        return super().get(request)


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
    

    @swagger_auto_schema(
    tags = ['User'],
    operation_summary= "SEARCH OR ALL USER\'S DETAILS", operation_description = 'Results in User\'s detailed list based on serach with username or select all with pagination', 
    responses={200: openapi.Response('LIST OF USER\'S', UserSerializer)})       
    def get(self, request):
        return super().get(request)


class CurrentUserDetailView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]  
    
    @swagger_auto_schema(
            tags = ['User'],
            operation_summary= "AUTHENTICATED USER\'S DETAILS", 
            operation_description = 'Provides details of current user with mini profile details of its follower and following')       
    def get(self, request):
        try:
            user = request.user
            serializer = self.serializer_class(user)
            return Response(serializer.data, status = 200)
        
        except Exception as e:
            return Response({'message' : str(e)}, status = 400)

        
        
class ArtistListView(generics.ListAPIView) :
    serializer_class = ArtistSerializer
    queryset = User.objects.filter(is_artist = True).order_by('id')
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 30

    @swagger_auto_schema(tags = ['Artist'], operation_summary= "ALL SINGER DETAILS", operation_description = 'Provides details of all the artists with their released Albums details and mini profile details of their follower and following')
    def get(self, request):
        return super().get(request)

class ArtistDetailView(generics.RetrieveAPIView):   
    serializer_class = ArtistSerializer
    queryset = User.objects.filter(is_artist = True)
    permission_classes = [permissions.IsAuthenticated]
   
    @swagger_auto_schema(tags = ['Artist'], operation_summary= "ARTIST DETAILS BY ID", operation_description = 'Provides details of single artists with his/her released Albums details and mini profile details of their follower and following')
    def get(self, request, pk):
        return super().get(request, pk)

class SendPasswordResetOTPView(generics.UpdateAPIView):
    serializer_class = MailOTPSerializer
    queryset = MailOTP.objects.all()
    http_method_names = ['put']
    
    @swagger_auto_schema(tags = ['Auth'], 
    operation_summary= "OTP FOR PASSWORD RESET", operation_description = 'Sends OTP to the provided email in request body', 
    request_body = EmailSerializer,
    responses={200: openapi.Response('OTP sent to your mail succesfully')})       
    def put(self, request):
        try:
            email = request.data['email']
            subject = 'Passwrod Reset Verfication Mail'
            body = CommonUtils.otp_generator()
            mail = Mail(subject, f'OTP: {str(body)}', [email])
            
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
                return Response({'message' : 'OTP sent to your mail succesfully'}, status=200)
            
            else :
                raise Exception('EMAIL NOT FOUND')
            
        except Exception as e:
            return Response({'message' : str(e)}, status = 400)
    

class resetPasswordTokenGenerationView(APIView):
    http_method_names = ['post']

    @swagger_auto_schema(tags = ['Auth'], 
    operation_summary= "GET RESET PASSWORD TOKEN", operation_description = 'Generates a Token for the User from email and otp sent to their email to allow password resetting', 
    request_body= EmailAndOTPSerializer,
    responses={
            200: openapi.Response(
                description="Token generated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'token': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }) 

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
    serializer_class = PasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(tags = ['Auth'], 
    operation_summary= "RESET PASSWORD", operation_description = 'JUST SEND YOUR NEW PASSWORD WITH THE TOKEN IN AUTHORIZATION HEADERS', 
    responses={
            200: 'password reset successfully'
        })
    def patch(self, request):
        try :
            user = UserUtils.getUserFromToken(request.headers['Authorization'].split(" ")[1])
            data = {'password' : request.data['password']}
            serializer = self.serializer_class(user, data = data, partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        
            return Response({'message' : 'password reset successfully'}, status = 200)
        except Exception as e:
            return Response({'message': str(e)}, status = 400)



class MailVerifyView(generics.GenericAPIView):
    http_method_names = ['get']
    queryset = None
    pagination_class = None
    @swagger_auto_schema(
        tags = ['Auth'], 
        operation_summary= "VERIFY EMAIL",
        operation_description = 'VERIFY YOUR MAIL BY CLICKING LINK SENT TO YOUR REGISTERED EMAIL', 
        responses={200: 'Verification Successful'},
        manual_parameters=[
            openapi.Parameter(
                'token',
                openapi.IN_QUERY,
                description="Verification Token",
                type=openapi.TYPE_STRING,  # Specify your choices here
            ),
        ],
        ) 
    def get(self, request, *args, **kwargs):
        try : 
            token = request.GET['token']
            token = MailVerificationToken.objects.filter(token = token).first()
            if not token:
                raise Exception("Invalid Link")

            if token.isExpired():
                raise Exception("Link Expired")  

            user = token.user_id
            user.is_verified = True
            user.save()
            token.delete()
            return  Response({'message' : 'Verification Successful'}, status=200)
        
        except Exception as e:
            return Response({'message' : str(e)}, status=400)

        
# class PatchLogoutView(DRFLogoutView):
#     """
#     Djano 5 does not have GET logout route anymore, so Django Rest Framework UI can't log out.
#     This is a workaround until Django Rest Framework implements POST logout.
#     Details: https://github.com/encode/django-rest-framework/issues/9206
#     """
#     http_method_names = ["get", "post", "options"]

#     def get(self, request, *args, **kwargs):
#         return super().post(request, *args, **kwargs)        


        
# SHORT NAMING :
user_profile_edit_view = UpdateUserProfileView.as_view()
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
mail_verification = MailVerifyView.as_view()
resend_mail_verification_link = ResendEmailVerificationLink.as_view()


