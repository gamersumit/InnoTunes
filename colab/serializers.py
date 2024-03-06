from rest_framework import serializers
from .models import Colab
from user.models import User

class ColabSerializer(serializers.ModelSerializer):
    colab_picture = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Colab
        fields = ['id', 'user_id', 'song_id', 'colab_name', 'colab_description', 'audio', 'video', 'audio_duration', 'colab_picture', 'created_at']
        read_only_fields = ['id', 'colab_picture', 'created_at']
    
    def get_colab_picture(self, obj):
        return obj.user_id.avatar
    