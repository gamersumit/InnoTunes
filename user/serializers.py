from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User, Followers
from utils.utils import UserUtils
from rest_framework.serializers import ValidationError

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, min_length = 8, write_only = True)
    total_followers = serializers.IntegerField(read_only = True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'username',
            'is_artist',
            'total_followers',
        ]
    
    def get_total_followers(self, artist):
        return Followers.get_total_followers()
    
    def validate_password(self, value):
       return UserUtils.validate_password(value)
    
class ArtistSerializer(serializers.ModelSerializer):
    total_followers = serializers.IntegerField(read_only = True)
    #List action
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'avatar',
            'total_followers',
            'total_albums',
        ]
    
    def get_total_followers(self, artist):
        return Followers.get_total_followers()

class FollowersDetailSerializer(serializers.ModelSerializer) :
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'avatar',
        ]
    
class FollowerSerializer(serializers.ModelSerializer):
    followers_detail = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Followers
        fields = [
            'id',
            'artist_id',
            'user_id',
            'followers_detail',
        ]
        read_only_fields = ['id', 'followers_detail']
        
    def get_followers_detail(self, obj):
        product = User.objects.get(id = obj.user_id.id)
        serializer = FollowersDetailSerializer(product)
        return serializer.data
    
    def validate(self, attributes):
        try :
            user = attributes['user_id']
            artist = attributes['artist_id']
            
            if user == artist :
                raise ValidationError('Follower and Artist cannot be the same')
            
            if Followers.objects.filter(user_id = user, artist_id = artist).exists() :
                raise ValidationError('User is already Following the given artist')
            
            return attributes
        
        except Exception as e :
            raise ValidationError(str(e))
            
          
        
# GET ACTION RETERIVE  -- ON ID
# fields  = [
#     {album1}, {album2} , {}
# ]

# ---- album structure on artist id---
# album = [
#     'id',
#     'album_name',
#     'album_picture',
#     'album_discription',
#     'credits', # ---- will see later
#     'total_duration',
#     'total_songs',
#     'total_likes',
# ]

# --- songs on album id ----
# songs = [
#     'id',

#     'song_name',
#     'song_image',
#     'song_discription',

#     'audio',
#     'video',
#     'audio_duration',

#     'genre',
#     'credits' -- will see it later ---
#     'date_added',
# ]