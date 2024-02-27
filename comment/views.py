from tkinter import E
from django.shortcuts import render

import comment
from .serializers import CommentSerializer, FollowerSerializer
from rest_framework import generics, viewsets
from .models import AlbumLikes, Comment, Followers
from rest_framework.response import Response
from utils.utils import UserUtils, CommonUtils
from rest_framework.permissions import IsAuthenticated
from user.permissions import *

##### Comment Releated views ########
class CommentViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsUserOwnerOrReadOnly]
    serializer_class = [CommentSerializer]
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']
    
    def get_queryset(self):
        try :
          user = self.request.data['user_id']
          return Comment.objects.filter(user_id = user)
        
        except :
          return {}

class CommentsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
      try :
        
        field = self.kwargs['field']
        id = self.kwargs['id']
        
        if field == 'user' :
          return Comment.objects.filter(user_id = id)
        
        if field == 'song' :
          return Comment.objects.filter(song_id = id)

        else :
          return {}
      
      except :
        return {}
        


##### FOllower Releated views ########
class FollowUnfollowView(generics.GenericAPIView):
    queryset = Followers.objects.all()
    serializer_class = FollowerSerializer
    permission_class = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]
    http_method_names = ['post', 'delete']
    
    def delete(self, request):
      try :
        Followers.objects.get(artist_id = request.data['artist_id'], user_id = request.data['user_id']).delete()
        return Response({'message' : 'request successful'}, status = 200)
      except Exception as e:
        return Response({'message' : str(e)}, status = 400)
      
class ListAllFollowersView(generics.ListAPIView):
    serializer_class = FollowerSerializer
    permission_class = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        id = self.kwargs.get('id')
        return Followers.objects.filter(artist_id = id)

##### FOllower Releated views ########
class LikeDislikeView(generics.GenericAPIView):
    queryset = AlbumLikes.objects.all()
    serializer_class = FollowerSerializer
    permission_class = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]
    http_method_names = ['post', 'delete']
    
    def delete(self, request):
      try :
        Followers.objects.get(album_id = request.data['album_id'], user_id = request.data['user_id']).delete()
        return Response({'message' : 'request successful'}, status = 200)
      
      except Exception as e:
        return Response({'message' : str(e)}, status = 400)
      
