from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User
from comment.serializers import FollowersDetailSerializer
from music.models import Album
from music.serializers import AlbumSerializer
from comment.models import Followers
from utils.utils import UserUtils
from rest_framework.serializers import ValidationError

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
            'is_artist',
            'total_followers',
            'total_following',
            'followers',
            'following',
        ]
        read_only_fields = ['id']
    
    def get_total_followers(self, user):
        return Followers.get_total_followers(user)
    
    def get_total_following(self, user):
        return Followers.get_total_following(user)
    
    def get_followers(self, user):
        users = [follower.user_id for follower in Followers.objects.filter(artist_id = user)]
        serializer = FollowersDetailSerializer(users, many = True)
        
        return serializer.data
    
    def get_following(self, user):
        users = [follower.artist_id for follower in Followers.objects.filter(artist_id = user)]
        
        serializer = FollowersDetailSerializer(users, many =True)
        return serializer.data
    
    def validate_password(self, value):
       return UserUtils.validate_password(value)
    
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
            'albums', # list of albums
        ]
    
    def get_total_followers(self, artist):
        return Followers.get_total_followers(artist)
    
    def get_total_following(self, artist):
        return Followers.get_total_following(artist)
    
    def get_followers(self, artist):
        artists = [follower.user_id for follower in Followers.objects.filter(artist_id = artist)]
        serializer = FollowersDetailSerializer(artists, many = True)
        return serializer.data
    
    def get_following(self, artist):
        artists = [follower.artist_id for follower in Followers.objects.filter(artist_id = artist)]
        serializer = FollowersDetailSerializer(artists, many = True)
        return serializer.data
    
    def get_albums(self, artist):
        albums = Album.objects.filter(artist_id = artist.id)
        serializer = AlbumSerializer(albums, many = True)
        return serializer.data
    
    def get_total_albums(self, artist):
        return Album.objects.filter(artist_id = artist.id).count()
