from rest_framework import serializers
from .models import Colab

class ColabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colab
        fields = '__all__'
        read_only_data = ['user_id', 'song_id']
        