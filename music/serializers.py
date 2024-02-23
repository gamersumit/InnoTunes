from rest_framework import serializers
from .models import *

# <! ---------- SONGS SERIALIZERS -----------!>
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

# <! ---------- PLAYLIST SERIALIZERS -----------!> 
class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'
        read_only_fields = ['id']

    
    def validate(self, attributes):
        try :
            if Playlist.objects.filter(title = attributes['title'], user_id = attributes['user_id']) :
                raise Exception('Playlist already exists')
            
            attributes['title'] = attributes['title'].title()
            return attributes

        except Exception as e :
            raise Exception(str(e))
        
   
class SongsInPlaylistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SongsInPlaylist
        fields = '__all__'
        read_only_fields = ['id']
        
        
# <! ---------- ALBUM SERIALIZERS -----------!> 
class AlbumSerializer(serializers.ModelSerializer):
    total_songs = serializers.IntegerField(default = 0)
    total_duration = serializers.DecimalField(default = 0, decimal_places = 2)
    
    class Meta:
        model = Album
        fields = '__all__'
        read_only_fields = ['id', 'total_songs', 'total_duration']
           
    def get_total_songs(self, attrs):   ## returns a list of count of songs in each album of an artist
      return Song.objects.filter(album_id = attrs['id'].id).count()       

    def get_total_duration(self, attrs):
        duration_list = [song.duration for song in (Song.object.filter(album_id = attrs['id'].id))] 
        duration = None # for now will have to calculate it
        return duration

class SongsInAlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = SongsInAlbum
        fields = '__all__'
        read_only_fields = ['id','song_id','album_id','total_songs']
        
    def get_total_songs(self, attrs):   ## total songs in an album
        songs_in_album = attrs.album_id 
        return songs_in_album.count()