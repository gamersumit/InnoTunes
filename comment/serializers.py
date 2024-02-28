from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import *
from user.models import User

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id']
        
class FollowersDetailSerializer(serializers.ModelSerializer) :
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'avatar',
        ]
    
class FollowerSerializer(serializers.ModelSerializer):
    followers_detail = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Followers
        fields = [
            'id',
            'artist_id',
            'user_id',
            'followers_detail',
        ]
        read_only_fields = ['id', 'followers_detail']
        
    def get_followers_detail(self, obj):
        user = User.objects.get(id = obj.user_id.id)
        serializer = FollowersDetailSerializer(user)
        return serializer.data
    
    def validate(self, attrs):
        try :
            if attrs['user'] == attrs['artist'] :
                raise ValidationError('Follower and Artist cannot be the same')
           
            return attrs
        
        except Exception as e :
            raise ValidationError(str(e))


# Likes --- album, playlist

class AlbumLikesSerializer(serializers.Serializer):
    class Meta:
        model = AlbumLikes
        fields = '__all__'
        read_only_fields = ['id']

class PlaylistLikesSerializer(serializers.Serializer):
    class Meta:
        model = PlaylistLikes
        fields = '__all__'
        read_only_fields = ['id']