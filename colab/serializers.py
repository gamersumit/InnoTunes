from rest_framework import serializers
from .models import Colab
from user.models import User


class ColabSerializer(serializers.ModelSerializer):
    song_name = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    # user_id = serializers.CurrentUserDefault()
    
    class Meta:
        model = Colab
        fields = ['id', 'user_id', 'song_id', 'song_name', 'comments', 'likes','colab_name', 'audio', 'video', 'audio_duration', 'colab_picture', 'created_at']
        read_only_fields = ['id', 'created_at', 'song_name', 'user_id', 'comments', 'likes']

    
    def get_colab_picture(self, obj):
        return obj.user_id.avatar
    
    def get_song_name(self, obj):
        return obj.song_id.song_name
    
    def get_likes(self, obj):
        return None
    
    def get_comments(self, obj):
        return None


class PostCollabSerializer(serializers.Serializer):
    song_id = serializers.CharField(max_length = 32, required = True)
    audio = serializers.FileField(required = True)
    video = serializers.FileField(required = False)
    colab_picture = serializers.ImageField(required = False)
    colab_name = serializers.CharField(max_length = 32, required = False)