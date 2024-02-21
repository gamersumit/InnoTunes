from rest_framework import serializers
from .models import Song, Playlist, SongsInPlaylist

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


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