from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User
from music.models import Album
from comment.models import Followers
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
            'avatar',
            'is_artist',
            'total_followers',
        ]
        read_only_fields = ['id']
    
    def get_total_followers(self, artist):
        return Followers.get_total_followers()
    
    def validate_password(self, value):
       return UserUtils.validate_password(value)
    
class ArtistSerializer(serializers.ModelSerializer):
    total_followers = serializers.SerializerMethodField(read_only = True)
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
            'total_albums',
            'albums', # list of albums
        ]
    
    def get_total_followers(self, artist):
        return Followers.get_total_followers(artist)
    
    def get_albums(self, artist):
        return Album.objects.filter(artist_id = artist.id)
    
    def get_total_albums(self, artist):
        print("#### ", artist)
        return Album.objects.filter(artist_id = artist.id).count()


          
        
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