from utils.utils import CommonUtils
from .serializers import *
from rest_framework import generics, viewsets
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user.permissions import *
from user.models import User
from user.serializers import UserMiniProfileSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

##### Comment Releated views ########
class CommentViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    http_method_names = ['post', 'put', 'delete']
    serializer_class = SongCommentSerializer

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return SongCommentSerializer
        elif self.action == 'create':
            return PostCommentSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return EditCommentSerializer
        return SongCommentSerializer
    
    def get_queryset(self):
      user = self.request.user
      self.request.data['user_id'] = user.id
      return Comment.objects.filter(user_id = user.id)
  
    @swagger_auto_schema(tags = ['Reach'], 
    operation_summary= "POST COMMENT", operation_description = 'User can comment on any song.', 
    responses={
            200: openapi.Response('COMMENT POSTED', SongCommentSerializer)
        })  
    def create(self, request, *args, **kwargs):
       self.serializer_class = SongCommentSerializer
       return super().create(request, *args, **kwargs)    

    @swagger_auto_schema(tags = ['Reach'], 
    operation_summary= "EDIT COMMENT", operation_description = 'User can edit their comments.', 
    responses={
            200: openapi.Response('COMMENT UPDATED', SongCommentSerializer)
        })  
    def update(self, request, *args, **kwargs):
       self.serializer_class = SongCommentSerializer
       return super().partial_update(request, *args, **kwargs)
    

    @swagger_auto_schema(tags = ['Reach'], 
    operation_summary= "EDIT COMMENT", operation_description = 'User can edit their comments.', 
    responses={ 204: 'Comment deleted successfully'})  
    def destroy(self, request, *args, **kwargs):
       return super().destroy(request, *args, **kwargs)

class SongCommentsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SongCommentSerializer
   
    def get_queryset(self):
      return Comment.objects.filter(song_id = self.kwargs.get('id'))

    @swagger_auto_schema(tags = ['Reach'], 
    operation_summary= "VIEW COMMENTS ON A SONG", operation_description = 'Return a paginated list of all the comments on a single song.')
    def get(self, request, *args, **kwargs):
       return  super().get(self, request, *args, **kwargs)
##### FOllower Releated views ########
class FollowUnfollowView(generics.GenericAPIView):
    queryset = Followers.objects.all()
    serializer_class = FollowerSerializer
    permission_class = [permissions.IsAuthenticated]
    http_method_names = ['post', 'delete']
    
    @swagger_auto_schema(tags = ['Reach'], 
    operation_summary= "FOLLOW", 
    operation_description = 'To FOLLOW a user. Takes artist_id as body who the user want to follow',
    responses={200: openapi.Response("success", FollowerSerializer)},
    request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'artist_id': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    def post(self, request):
      try :
        request.data['user_id'] = request.user.id
        return CommonUtils.Serialize(request.data, self.serializer_class)
      except Exception as e:
        return Response({'message' : str(e)}, status = 400)

    @swagger_auto_schema(tags = ['Reach'], 
    operation_summary= "UNFOLLOW", 
    operation_description = 'To unfollow a user. Takes artist_id as body who the user want to unfollow',
    responses= {200: 'request successful'},
    request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'artist_id': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )  
    def delete(self, request):
      try :
        Followers.objects.get(artist_id = request.data['artist_id'], user_id = request.user.id).delete()
        return Response({'message' : 'request successful'}, status = 200)
      
      except Exception as e:
        return Response({'message' : str(e)}, status = 400)
      
class ListAllFollowersView(generics.ListAPIView):
    serializer_class = UserMiniProfileSerializer
    permission_class = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        id = self.kwargs.get('id')
        user = User.objects.get(id = id)
        users =  user.following.values_list('user_id', flat=True)
        return User.objects.filter(id__in=users)

    @swagger_auto_schema(tags = ['Reach'], 
    operation_summary= "FOLLOWERS LIST", operation_description = 'Return a paginated list of all the followers of a user by its user-id')
    def get(self, request, *args, **kwargs):
       return  super().get(self, request, *args, **kwargs)

class ListAllFollowingView(generics.ListAPIView):
    serializer_class = UserMiniProfileSerializer
    permission_class = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        id = self.kwargs.get('id')
        user = User.objects.get(id = id)
        users =  user.following.values_list('artist_id', flat=True)
        return User.objects.filter(id__in=users)
    

    @swagger_auto_schema(tags = ['Reach'], 
    operation_summary= "FOLLOWING LIST", operation_description = 'Return a paginated list of all the user, followed a user by user-id')
    def get(self, request, *args, **kwargs):
       return  super().get(self, request, *args, **kwargs)

##### Likes Releated views ########
class AlbumLikeDislikeView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = AlbumLikes.objects.all()
    serializer_class = AlbumLikesSerializer
    permission_class = [permissions.IsAuthenticated]
    http_method_names = ['post', 'delete']
    
    @swagger_auto_schema(tags = ['Reach'], 
    operation_summary= "DISLIKE ALBUM", 
    operation_description = 'Their is no count of dislikes on a album at backend. Here dislike indicates that user wants to remove this album from their liked album\'s list if present.',
    responses= {200: 'request successful', 201 : 'already disliked'},
    request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'album_id': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    def delete(self, request):
      try :
        if AlbumLikes.objects.filter(album_id = request.data['album_id'], user_id = request.user.id).exists():
          AlbumLikes.objects.get(album_id = request.data['album_id'], user_id = request.user.id).delete()
          return Response({'message' : 'request successful'}, status = 200)
        return Response({'message' : 'already disliked'}, status = 201)
      
      except Exception as e:
        return Response({'message' : str(e)}, status = 400)
    
    @swagger_auto_schema(tags = ['Reach'], 
    operation_summary= "LIKE ALBUM", 
    operation_description = 'To LIKE AN ALBUM',
    responses={200: openapi.Response("success", AlbumLikesSerializer)},
    request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'album_id': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    def post(self, request, *args, **kwargs):
      request.data['user_id'] = request.user.id
      return super().post(self, request, *args, **kwargs)

class PlaylistLikeDislikeView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = PlaylistLikes.objects.all()
    serializer_class = PlaylistLikesSerializer
    permission_class = [permissions.IsAuthenticated]
    http_method_names = ['post', 'delete']
    

    @swagger_auto_schema(tags = ['Reach'], 
    operation_summary= "DISLIKE PLAYLIST", 
    operation_description = 'Their is no count of dislikes on a playlist at backend. Here dislike indicates that user wants to remove this playlist from their liked playlist\'s list if present.',
    responses= {200: 'request successful', 201 : 'already disliked'},
    request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'playlist_id': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    def delete(self, request):
      try :
        if PlaylistLikes.objects.filter(playlist_id = request.data['playlist_id'], user_id = request.user.id).exists() :
          PlaylistLikes.objects.get(playlist_id = request.data['playlist_id'], user_id = request.user.id).delete()
          return Response({'message' : 'request successful'}, status = 200)
        return Response({'message' : 'already disliked'}, status = 201)
      except Exception as e:
        return Response({'message' : str(e)}, status = 400)
      

    @swagger_auto_schema(tags = ['Reach'], 
    operation_summary= "LIKE PLAYLIST", 
    operation_description = 'To LIKE A PLAYLIST',
    responses={200: openapi.Response("success", PlaylistLikesSerializer)},
    request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'playlist_id': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    def post(self, request, *args, **kwargs):
      request.data['user_id'] = request.user.id
      return super().post(self, request, *args, **kwargs)
      
      
class SongLikeDislikeView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = SongLikes.objects.all()
    serializer_class = SongLikesSerializer
    permission_class = [permissions.IsAuthenticated]
    http_method_names = ['post', 'delete']
    
    @swagger_auto_schema(tags = ['Reach'], 
    operation_summary= "DISLIKE SONG", 
    operation_description = 'Their is no count of dislikes on a song at backend. Here dislike indicates that user wants to remove this song from their liked song list if present.',
    responses= {200: 'request successful', 201 : 'already disliked'},
    request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'song_id': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    def delete(self, request):
      try :
        if SongLikes.objects.filter(song_id = request.data['song_id'], user_id = request.user.id).exists():
          SongLikes.objects.get(song_id = request.data['song_id'], user_id = request.user.id).delete()
          return Response({'message' : 'request successful'}, status = 200)
        return Response({'message' : 'already disliked'}, status = 201)
      except Exception as e:
        return Response({'message' : str(e)}, status = 400)
      
    

    @swagger_auto_schema(tags = ['Reach'], 
    operation_summary= "LIKE SONG", 
    operation_description = 'To LIKE A SONG',
    responses={200: openapi.Response("success", SongLikesSerializer)},
    request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'song_id': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    def post(self, request, *args, **kwargs):
      request.data['user_id'] = request.user.id
      return super().post(self, request, *args, **kwargs)