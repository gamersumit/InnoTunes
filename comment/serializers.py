from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import *
from user.models import User


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'song_id': {'write_only': True},
        }
        
class SongCommentSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'user_info']
        extra_kwargs = {
            'song_id': {'write_only': True},
            'user_id': {'write_only': True}
        }
    
    def get_user_info(self, obj):
        user = obj.user_id
        from user.serializers import UserMiniProfileSerializer
        return UserMiniProfileSerializer(user).data


class EditCommentSerializer(serializers.Serializer):
    description = serializers.CharField(max_length = 1000000)
    
class PostCommentSerializer(EditCommentSerializer):
    song_id = serializers.CharField(max_length = 32)


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
        user = obj.user_id
        from user.serializers import UserMiniProfileSerializer
        serializer = UserMiniProfileSerializer(user)
        return serializer.data
    
    def validate(self, attrs):
        try :
            
            if attrs['user_id'] == attrs['artist_id'] :
                raise ValidationError('Follower and Artist cannot be the same')
            
            return attrs
        
        except Exception as e :
            raise ValidationError(str(e))


# Likes --- album, playlist

class AlbumLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumLikes
        fields = '__all__'
        read_only_fields = ['id']

class PlaylistLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistLikes
        fields = '__all__'
        read_only_fields = ['id']

class SongLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongLikes
        fields = '__all__'
        read_only_fields = ['id']
        
    def validate(self, attrs):
        return attrs