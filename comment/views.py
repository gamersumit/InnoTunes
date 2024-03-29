from utils.utils import CommonUtils
from .serializers import *
from rest_framework import generics, viewsets
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user.permissions import *

##### Comment Releated views ########
class CommentViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsUserOwnerOrReadOnly]
    serializer_class = SongCommentSerializer
    lookup_field = 'pk'
    http_method_names = ['post', 'put', 'delete']
    
    def get_queryset(self):
        try :
          user = self.request.data['user_id']
          print(Comment.objects.filter(user_id = user), "queryset")
          return Comment.objects.filter(user_id = user)
  
        except :
          return []

class CommentsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SongCommentSerializer
   
    def get_queryset(self):
      return Comment.objects.filter(song_id = self.kwargs.get('id'))
        
##### FOllower Releated views ########
class FollowUnfollowView(generics.GenericAPIView):
    queryset = Followers.objects.all()
    serializer_class = FollowerSerializer
    permission_class = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]
    http_method_names = ['post', 'delete']
    
    def post(self, request):
      try :
        return CommonUtils.Serialize(request.data, self.serializer_class)
      except Exception as e:
        return Response({'message' : str(e)}, status = 400)
      
    def delete(self, request):
      try :
        Followers.objects.get(artist_id = request.data['artist_id'], user_id = request.data['user_id']).delete()
        return Response({'message' : 'request successful'}, status = 200)
      except Exception as e:
        return Response({'message' : str(e)}, status = 400)
      
class ListAllFollowersView(generics.ListAPIView):
    serializer_class = FollowersDetailSerializer
    permission_class = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        id = self.kwargs.get('id')
        return [follower.user_id for follower in Followers.objects.filter(artist_id = id)]

class ListAllFollowingView(generics.ListAPIView):
    serializer_class = FollowersDetailSerializer
    permission_class = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        id = self.kwargs.get('id')
        return [follower.artist_id for follower in Followers.objects.filter(user_id = id)]

##### Likes Releated views ########
class AlbumLikeDislikeView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = AlbumLikes.objects.all()
    serializer_class = AlbumLikesSerializer
    permission_class = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]
    http_method_names = ['post', 'delete']
    
    def delete(self, request):
      try :
        if AlbumLikes.objects.filter(album_id = request.data['album_id'], user_id = request.data['user_id']).exists():
          AlbumLikes.objects.get(album_id = request.data['album_id'], user_id = request.data['user_id']).delete()
          return Response({'message' : 'request successful'}, status = 200)
        return Response({'message' : 'already disliked'}, status = 201)
      
      except Exception as e:
        return Response({'message' : str(e)}, status = 400)
      

class PlaylistLikeDislikeView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = PlaylistLikes.objects.all()
    serializer_class = PlaylistLikesSerializer
    permission_class = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]
    http_method_names = ['post', 'delete']
    
    def delete(self, request):
      try :
        if PlaylistLikes.objects.filter(playlist_id = request.data['playlist_id'], user_id = request.data['user_id']).exists() :
          PlaylistLikes.objects.get(playlist_id = request.data['playlist_id'], user_id = request.data['user_id']).delete()
          return Response({'message' : 'request successful'}, status = 200)
        return Response({'message' : 'already disliked'}, status = 201)
      except Exception as e:
        return Response({'message' : str(e)}, status = 400)
      
      
class SongLikeDislikeView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = SongLikes.objects.all()
    serializer_class = SongLikesSerializer
    permission_class = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]
    http_method_names = ['post', 'delete']
    
    def delete(self, request):
      try :
        if SongLikes.objects.filter(song_id = request.data['song_id'], user_id = request.data['user_id']).exists():
          SongLikes.objects.get(song_id = request.data['song_id'], user_id = request.data['user_id']).delete()
          return Response({'message' : 'request successful'}, status = 200)
        return Response({'message' : 'already disliked'}, status = 201)
      except Exception as e:
        return Response({'message' : str(e)}, status = 400)