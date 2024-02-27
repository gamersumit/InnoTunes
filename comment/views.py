from django.shortcuts import render

import comment
from .serializers import CommentSerializer
from rest_framework import generics, viewsets
from .models import Comment
from rest_framework.response import Response
from utils.utils import UserUtils, CommonUtils
from rest_framework.permissions import IsAuthenticated
from user.permissions import *
# Create your views here.

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
        
        