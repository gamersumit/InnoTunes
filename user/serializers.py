from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import *
from music.models import Album
from music.serializers import AlbumSerializer
from comment.models import Followers
from utils.utils import CommonUtils, UserUtils
from rest_framework.serializers import ValidationError



class UserMiniProfileSerializer(serializers.ModelSerializer) :
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'avatar',
            'is_deleted',
            'status',
        ]
        
    def to_representation(self, obj):
        ret = super().to_representation(obj)
        if ret['is_deleted'] : 
            ret['username'] = 'innouser'
        return ret

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length = 8, write_only = True)
    total_followers = serializers.SerializerMethodField(read_only = True)
    total_following = serializers.SerializerMethodField(read_only = True)
    followers = serializers.SerializerMethodField(read_only = True)
    following = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'username',
            'avatar',
            'status',
            'is_artist',
            'is_deleted',
            'total_followers',
            'total_following',
            'followers',
            'following',
        ]
        read_only_fields = ['id', 'is_deleted', 'status']
        
    
    def to_representation(self, obj):
        ret = super().to_representation(obj)
        if ret['is_deleted'] : 
            ret['username'] = 'innouser'
            
        if not ret['avatar']:
            ret['avatar'] = 'https://cdn.vectorstock.com/i/1000v/43/94/default-avatar-photo-placeholder-icon-grey-vector-38594394.jpg'
        return ret
        
    
    def get_total_followers(self, user):
        return Followers.get_total_followers(user)
    
    def get_total_following(self, user):
        return Followers.get_total_following(user)
    
    def get_followers(self, user):
        users = user.following.values_list('user_id', flat=True)
        users = User.objects.filter(id__in=users)
        serializer = UserMiniProfileSerializer(users, many = True)
        return serializer.data
    
    def get_following(self, user):
        users = user.follower.values_list('artist_id', flat=True)
        users = User.objects.filter(id__in=users)
        serializer = UserMiniProfileSerializer(users, many =True)
        return serializer.data
    
    def run_validation(self, data):
        return super().to_internal_value(data)
    
    def validate_password(self, value):
       return UserUtils.validate_password(value)

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'avatar',
        ]
        
        
class ArtistSerializer(serializers.ModelSerializer):
    total_followers = serializers.SerializerMethodField(read_only = True)
    total_following = serializers.SerializerMethodField(read_only = True)
    followers = serializers.SerializerMethodField(read_only = True)
    following = serializers.SerializerMethodField(read_only = True)
    total_albums = serializers.SerializerMethodField(read_only = True)
    albums = serializers.SerializerMethodField(read_only = True)
    
    #List action
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'avatar',
            'total_followers',
            'total_following',
            'followers',
            'following',
            'total_albums',
            'status',
            'is_deleted',
            'albums', # list of albums
        ]
    
    def to_representation(self, obj):
        ret = super().to_representation(obj)
        if ret['is_deleted'] : 
            ret['username'] = 'innouser'
        if not ret['avatar']:
            ret['avatar'] = 'https://cdn.vectorstock.com/i/1000v/43/94/default-avatar-photo-placeholder-icon-grey-vector-38594394.jpg'
        return ret
    
    def get_total_followers(self, artist):
        return Followers.get_total_followers(artist)
    
    def get_total_following(self, artist):
        return Followers.get_total_following(artist)
    
    def get_followers(self, artist):
        users = artist.following.values_list('user_id', flat=True)
        users = User.objects.filter(id__in=users)
        serializer = UserMiniProfileSerializer(users, many = True)
        return serializer.data
    
    def get_following(self, artist):
        users = artist.follower.values_list('artist_id', flat=True)
        users = User.objects.filter(id__in=users)
        serializer = UserMiniProfileSerializer(users, many =True)
        return serializer.data
    
    def get_albums(self, artist):
        albums = Album.objects.filter(artist_id = artist.id)
        serializer = AlbumSerializer(albums, many = True)
        return serializer.data
    
    def get_total_albums(self, artist):
        return Album.objects.filter(artist_id = artist.id).count()


class MailOTPSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MailOTP
        fields = '__all__'
        read_only_fields = ['id', 'updated_at']


class RegisterSerializer(UserSerializer):
    avatar = serializers.ImageField(required=False)

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, max_length = 128)
class EmailAndOTPSerializer(serializers.Serializer):    
    email = serializers.EmailField(required=True)
    otp = serializers.IntegerField(required=True)
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length = 100)
    password = serializers.CharField(required=True, max_length = 128)

class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField(max_length = 128)
    user_info = UserSerializer()
    liked_songs = serializers.ListField(child=serializers.CharField(max_length=100))  
    liked_albums = serializers.ListField(child=serializers.CharField(max_length=100))  
    liked_playlists = serializers.ListField(child=serializers.CharField(max_length=100)) 