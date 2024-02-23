from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from music.models import Album, SongsInAlbum
from .serializers import AlbumSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utils.utils import UserUtils
# Create your views here.

# class AlbumViewSet(viewsets.ViewSet):
#     queryset = Album.objects.all()
#     serializer_class = AlbumSerializer
    
#     def create(self, request):
#         return Response({'status': True, 'message': 'Success'}, status = status.HTTP_200_OK)        
    
#     def list(self, request):
#         return Response({'status': True, 'message': 'Success'}, status = status.HTTP_200_OK)

class AlbumViewSet(viewsets.ViewSet):    
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'delete']
    
    def get_queryset(self):
        if self.action in ['post', 'destroy']:
            try:
                token = self.request.headers['Authorization'].split(' ')[1]
                user = UserUtils.getUserFromToken(token)
                self.request.data['user_id'] = user
                isArtist = user.isArtist
                if isArtist:        ## is user is artist, CRUD can be performed
                    return Album.objects.filter(user_id = user)  
                else:
                    raise Exception("User not an artist")   ## if normal user tries to perform post or destroy
            except Exception as e:
                raise Exception(str(e))
        else:
            try:
                token = self.request.headers['Authorization'].split(' ')[1]
                user = UserUtils.getUserFromToken(token)
                self.request.data['user_id'] = user
                return Album.objects.filter(user_id = user.id)
            except Exception as e:
                raise Exception(str(e))
        
class SongsInAlbumViewSet(viewsets.ViewSet):    
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'put']
    lookup_field = 'pk'
    
    def get_queryset(self):
        if self.action in ['create', ' destroy', 'partial_update']:
            try:
                token = self.request.headers['Authorization'].split(' ')[1]
                user = UserUtils.getUserFromToken(token)
                isArtist = user.isArtist
                album_id = self.request.data['album_id']
                if isArtist is not None:
                    return SongsInAlbum.objects.filter(album_id = album_id)
                else:
                    raise Exception("Not a registered user")                
            except Exception as e:
                raise Exception(str(e))
        else:
            try:
                token = self.request.headers['Authorization'].split(' ')[1]
                user = UserUtils.getUserFromToken(token)
                album_id = self.request.data['album_id']
                return SongsInAlbum.objects.filter(album_id = album_id)
            
            except Exception as e:
                raise Exception(str(e))
        