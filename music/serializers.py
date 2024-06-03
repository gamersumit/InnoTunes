from email.policy import default
from xml.dom import ValidationErr
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import *
from comment.models import SongLikes, Comment
from cloudinary import uploader
from utils.utils import CommonUtils

class GnereSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Genre
        fields = ['genre', 'genre_picture']


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




class PostSongSerializer(serializers.Serializer):
    # genre choices
    genre_choices = Genre.objects.all().values_list('genre', 'genre')


    song_name = serializers.CharField(max_length = 500, required = True)
    song_discription = serializers.CharField(max_length = 100000, required = False)
    song_pitcure = serializers.ImageField(required = True)
    audio = serializers.FileField(required = True)
    video = serializers.FileField(required = False)
    genre = serializers.ChoiceField(choices = genre_choices, required = True)
    lyrics = serializers.CharField(required = False, max_length = 100000)
    credits = serializers.CharField(required = False, max_length = 10000)



# <! ---------- PLAYLIST SERIALIZERS -----------!> 
class PlaylistSerializer(serializers.ModelSerializer):
    total_songs = serializers.SerializerMethodField(read_only = True)
    playlist_duration = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Playlist
        fields = '__all__'
        read_only_fields = ['id', 'total_songs', 'playlist_duration']

    def get_total_songs(self, obj):
        return SongsInPlaylist.objects.filter(playlist_id = obj.id).count()
    
    def get_playlist_duration(self, obj):
        duration = sum([song.song_id.audio_duration for song in (SongsInPlaylist.objects.filter(playlist_id = obj.id))])
        return duration if duration is not None else 0



class PostPlaylistSerializer(serializers.Serializer):
    playlist_name = serializers.CharField(max_length = 50)
    playlist_picture = serializers.FileField(required = True)
    is_global = serializers.BooleanField(default = False, required = False)
    songs = serializers.ListField(
        child=serializers.CharField(max_length = 32),
        allow_empty=True,
        required=False
        )

class EditPlaylistSerializer(PostPlaylistSerializer):
    playlist_name = serializers.CharField(max_length = 50, required = False)
    

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
        
class EditRecentSongsSeriailizer(serializers.Serializer):
    song_id = serializers.CharField(max_length = 32)
# <! ---------- ALBUM SERIALIZERS -----------!> 
class AlbumSerializer(serializers.ModelSerializer):
    total_songs = serializers.SerializerMethodField(read_only = True)
    album_duration = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Album
        fields = '__all__'
        read_only_fields = ['id', 'total_songs', 'album_duration']
           
    def get_total_songs(self, obj):   ## returns a list of count of songs in each album of an artist
      return SongsInAlbum.objects.filter(album_id = obj.id).count()       

    def get_album_duration(self, obj):
        duration = sum([song.song_id.audio_duration for song in (SongsInAlbum.objects.filter(album_id = obj.id))])
        return duration if duration is not None else 0
    


class PostAlbumSerializer(serializers.Serializer):
    album_name = serializers.CharField(max_length = 200)
    album_description = serializers.CharField(max_length = 50000, required = False)
    album_picture = serializers.FileField(required = False)
    

class EditAlbumSerializer(PostAlbumSerializer):
    album_name = serializers.CharField(max_length = 200, required = False)


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




class CurrentlyPlayingSerializer(serializers.ModelSerializer):
    song_name = serializers.SerializerMethodField()
    song_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = CurrentlyPlaying
        fields = '__all__'
    
    
    def get_song_name(self, obj):
        return obj.song_id.song_name
        
    def get_song_picture(self, obj):
        return obj.song_id.song_picture