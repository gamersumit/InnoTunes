from xml.dom import ValidationErr
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import *
from cloudinary import uploader
from utils.utils import CommonUtils
# <! ---------- SONGS SERIALIZERS -----------!>
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'audio_duration']
        

# <! ---------- PLAYLIST SERIALIZERS -----------!> 
class PlaylistSerializer(serializers.ModelSerializer):
    total_songs = serializers.SerializerMethodField(default = 0)
    class Meta:
        model = Playlist
        fields = '__all__'
        read_only_fields = ['id', 'total_songs']

    def get_total_songs(self, obj):
        return SongsInPlaylist.objects.filter(playlist_id = obj.id).count()
        

class SongsInPlaylistSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = SongsInPlaylist
        fields = '__all__'
        read_only_fields = ['id', 'total_songs']
        
        
# <! ---------- ALBUM SERIALIZERS -----------!> 
class AlbumSerializer(serializers.ModelSerializer):
    total_songs = serializers.SerializerMethodField(read_only = True)
    # total_duration = serializers.DecimalField(default = 0, decimal_places = 2, max_digits=2)
    
    class Meta:
        model = Album
        fields = '__all__'
        read_only_fields = ['id', 'total_songs']
           
    def get_total_songs(self, obj):   ## returns a list of count of songs in each album of an artist
      return SongsInAlbum.objects.filter(album_id = obj.id).count()       

    # def get_total_duration(self, attrs):
    #     duration_list = [song.duration for song in (Song.object.filter(album_id = attrs['id'].id))] 
    #     duration = 10.20 # for now will have to calculate it
    #     return duration
    
    
    
   
class SongsInAlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = SongsInAlbum
        fields = '__all__'
        read_only_fields = ['id']
        