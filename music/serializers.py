from email.policy import default
from xml.dom import ValidationErr
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import *
from cloudinary import uploader
from utils.utils import CommonUtils
# <! ---------- SONGS SERIALIZERS -----------!>
class SongSerializer(serializers.ModelSerializer):
    album_name = serializers.SerializerMethodField(default = 'Single')
    class Meta:
        model = Song
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'album_name']
        
    def get_album_name(self, obj):
        try :
            album =  SongsInAlbum.objects.get(song_id = obj.id)
            album = Album.objects.get(id = album.album_id)
            return album.album_name
        except :
            return 'Single'

# <! ---------- PLAYLIST SERIALIZERS -----------!> 
class PlaylistSerializer(serializers.ModelSerializer):
    total_songs = serializers.SerializerMethodField(default = 0)
    playlist_duration = serializers.SerializerMethodField(default = 0)
    
    class Meta:
        model = Playlist
        fields = '__all__'
        read_only_fields = ['id', 'total_songs', 'playlist_duration']

    def get_total_songs(self, obj):
        return SongsInPlaylist.objects.filter(playlist_id = obj.id).count()
    
    def get_playlist_duration(self, obj):
        duration = sum([song.song_id.audio_duration for song in (SongsInPlaylist.objects.filter(playlist_id = obj.id))])
        return duration   

class SongsInPlaylistSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = SongsInPlaylist
        fields = '__all__'
        read_only_fields = ['id', 'total_songs']

class RecentSongsSerializer(serializers.ModelSerializer):     
    class Meta:
        model = RecentSongs
        fields = '__all__'
        read_only_fields = ['id', 'last_played_at']
    
# <! ---------- ALBUM SERIALIZERS -----------!> 
class AlbumSerializer(serializers.ModelSerializer):
    total_songs = serializers.SerializerMethodField(read_only = True)
    album_duration = serializers.SerializerMethodField(default = 0)
    
    class Meta:
        model = Album
        fields = '__all__'
        read_only_fields = ['id', 'total_songs', 'album_duration']
           
    def get_total_songs(self, obj):   ## returns a list of count of songs in each album of an artist
      return SongsInAlbum.objects.filter(album_id = obj.id).count()       

    def get_album_duration(self, obj):
        print([song.song_id.audio_duration for song in (SongsInAlbum.objects.filter(album_id = obj.id))])
        duration = sum([song.song_id.audio_duration for song in (SongsInAlbum.objects.filter(album_id = obj.id))])
        print("***********", duration)
        return duration
    

class SongsInAlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = SongsInAlbum
        fields = '__all__'
        read_only_fields = ['id']
    
    def validate(self, attrs):
        try :
            artist1 = attrs['album_id'].artist_id
            artist2 = attrs['song_id'].artist_id

            if artist1 == artist2:
                return attrs
            else :
                raise ValidationError("SONG and ALBUM must belong to same artist")
        except Exception as e:
            raise ValidationError(str(e))