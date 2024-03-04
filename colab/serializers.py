from rest_framework import serializers
from .models import Colab
from user.models import User

class ColabSerializer(serializers.ModelSerializer):
    
    album_name = serializers.CharField(required=False, max_length=255, allow_null=True, allow_blank=True)
    genre = serializers.CharField( required=False, max_length=100, allow_null=True, allow_blank=True)
    lyrics = serializers.CharField( required=False, max_length = 2000, allow_null=True, allow_blank=True)
    credits = serializers.CharField( required=False, max_length=255, allow_null=True, allow_blank=True)

    class Meta:
        model = Colab
        fields = ['id', 'user_id', 'song_id', 'album_name', 'song_name', 'song_picture', 'song_description', 'audio', 'video', 'audio_duration', 'genre', 'lyrics', 'credits', 'created_at']
        read_only_data = ['genre', 'lyrics', 'credits', 'album_name']
    
        
