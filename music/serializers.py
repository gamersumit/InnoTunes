from email.policy import default
from xml.dom import ValidationErr
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import *
from comment.models import SongLikes, Comment
from cloudinary import uploader
from utils.utils import CommonUtils
# <! ---------- SONGS SERIALIZERS -----------!>
class SongSerializer(serializers.ModelSerializer):
    album_name = serializers.SerializerMethodField(default = 'Single')
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Song
        fields = ['id', 'created_at', 'album_name', 'likes', 'comments', 'artist_id', 'song_name', 'song_picture', 'song_description', 'audio', 'video', 'audio_duration', 'genre', 'lyrics', 'credits']
        read_only_fields = ['id', 'created_at', 'album_name', 'likes', 'comments']
        
    def get_album_name(self, obj):
        try :
            album =  SongsInAlbum.objects.get(song_id = obj.id)
            album = Album.objects.get(id = album.album_id)
            return album.album_name
        except :
            return 'Single'
        
    def get_likes(self, obj):
        return SongLikes.objects.filter(song_id = obj.id).count()
    
    def get_comments(self, obj):
        return Comment.objects.filter(song_id = obj.id).count()

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
        read_only_fields = ['id']

class RecentSongsSerializer(serializers.ModelSerializer):     
    class Meta:
        model = RecentSongs
        fields = ['song_id', 'user_id']
        extra_kwargs = {
            'song_id': {'write_only': True},
            'user_id': {'write_only': True},
        }
        
    
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
        duration = sum([song.song_id.audio_duration for song in (SongsInAlbum.objects.filter(album_id = obj.id))])
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

class GlobalPlaylistSerializer(serializers.ModelSerializer):
    total_songs = serializers.SerializerMethodField(default = 0)
    playlist_duration = serializers.SerializerMethodField(default = 0)
    class Meta:
        model = Playlist
        fields = ['id', 'playlist_name', 'playlist_picture', 'total_songs', 'playlist_duration', 'is_global']
        
    def validate(self, data):   ## validates playlist name
        if data.get('is_global'):
            # If the playlist is global, ensure that the playlist_name is unique globally
            if Playlist.objects.filter(playlist_name=data['playlist_name']).exists():
                raise serializers.ValidationError("Playlist with this name already exists globally.")
        return data
    def get_total_songs(self, obj):
        return SongsInPlaylist.objects.filter(playlist_id = obj.id).count()
    
    def get_playlist_duration(self, obj):
        duration = sum([song.song_id.audio_duration for song in (SongsInPlaylist.objects.filter(playlist_id = obj.id))])
        return duration   
        

class GlobalSongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id','artist_id', 'title', 'credits', 'song_picture', 'song_duration']
class SongsInGlobalPlaylistSerializer(serializers.ModelSerializer):
    songs = GlobalSongsSerializer(many = True, read_only = True)
    class Meta:
        model = SongsInPlaylist
        fields = '__all__'
        read_only_fields = ['id', 'songs']