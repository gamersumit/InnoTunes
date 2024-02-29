from collections import UserDict
from curses.ascii import SO
from rest_framework.views import APIView
from .models import *
from .permissions import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import viewsets, generics
from rest_framework import permissions
from utils.utils import CommonUtils, UserUtils
from user.permissions import *
from music import serializers

# Create your views here.

# <! ---------------- songs views ------------------ !>
# Add a song view


class SongCreateView(generics.CreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated, IsArtistOwnerOrReadOnly]
    
    def post(self, request):
        try :
            CommonUtils.Update_Create(request, ['song_picture', 'audio', 'video'])
            return CommonUtils.Serialize(request.data, SongSerializer)
            
        except Exception as e:
            return Response({'message' : str(e)}, status = 400)

# list all songs
class SongListView(ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
           
            field = self.kwargs.get('field', None)
            id = self.kwargs.get('id')
            
            if not field:
                return Song.objects.all()
            elif field == 'artist':
                model = Song
                return model.objects.filter(artist_id=id)
            elif field == 'album':
                model = SongsInAlbum
                return model.objects.filter(album_id=id)
            elif field == 'playlist':
                model = SongsInPlaylist
                return model.objects.filter(playlist_id=id)
            else:
                raise Exception('Invalid Url : /songs/!/!')

     
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=200)

# <! ---------------- Playlist views ------------------ !>
#  playlist CRUDS(these cruds are not for songs inside playlist) view
class PlaylistViewSet(viewsets.ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        try:
            return Playlist.objects.filter(user_id=self.request.data['owner_id'])

        except Exception as e:
            return None
       
    def create(self, request):
        try :
            CommonUtils.Update_Create(request, ['playlist_picture'])
            return CommonUtils.Serialize(request.data, PlaylistSerializer)
            
        except Exception as e:
            return Response({'message' : str(e)}, status = 400)    
    
    def update(self, request):
        try :
            CommonUtils.Update_Create(request, ['playlist_picture'])
            return CommonUtils.Serialize(request.data, PlaylistSerializer)
            
        except Exception as e:
            return Response({'message' : str(e)}, status = 400)
        
        
# album Cruds(these cruds are not for songs inside album)
class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    permission_classes = permissions.IsAuthenticated, IsArtistOwnerOrReadOnly
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        try:
            
            id = self.request.data['artist_id']
            return Album.objects.filter(artist_id = id)
        
        except Exception as e:
            return None
        
        
    def create(self, request):
        try :
            CommonUtils.Update_Create(request, ['album_picture'])
            return CommonUtils.Serialize(request.data, AlbumSerializer)
            
        except Exception as e:
            return Response({'message' : str(e)}, status = 400)    
    
 
    def update(self, request):
        try :
            CommonUtils.Update_Create(request, ['album_picture'])
            return CommonUtils.Serialize(request.data, AlbumSerializer)
            
        except Exception as e:
            return Response({'message' : str(e)}, status = 400)
            

# post and delete operations for songs inside a playlist

class AddDeleteSongsFromPlaylistView(generics.GenericAPIView):
    queryset = SongsInPlaylist.objects.all()
    serializer_class = SongsInPlaylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsPlaylistOwnerOrReadOnly]

    def post(self):
        try:

            data = {}
            data['song_id'] = self.kwargs.get('song_id')
            data['playlist_id'] = self.kwargs.get('playlist_id')

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)

            serializer.save()
            return Response({'status': True, 'message': 'Songs Added to Playlist Successfuly'}, status=200)

        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=400)

    def delete(self):
        try:
            data = {}
            data['playlist_id'] = self.kwargs.get('playlist_id')
            data['song_id'] = self.kwargs.get('song_id')

            SongsInPlaylist.objects.get(**data).delete()

            return Response({'status': True, 'message': 'Song Removed from Playlist Successfuly'}, status=200)

        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=400)


# post and delete operations for songs inside a album
class AddDeleteSongsFromAlbumView(generics.GenericAPIView):
    queryset = SongsInAlbum.objects.all()
    serializer_class = SongsInAlbumSerializer
    permission_classes = [permissions.IsAuthenticated, IsAlbumOwnerOrReadOnly]

    def post(self, request):
        try:

            # data = {}
            # data['song_id'] = self.kwargs.get('song_id')
            # data['album_id'] = self.kwargs.get('album_id')
            
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save()
            return Response({'status': True, 'message': 'Songs Added to album Successfuly'}, status=200)

        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=400)

    def delete(self, request):
        try:
            data = {}
            data['album_id'] = self.kwargs.get('album_id')
            data['song_id'] = self.kwargs.get('song_id')

            SongsInAlbum.objects.get(**data).delete()

            return Response({'status': True, 'message': 'Song Removed from album Successfuly'}, status=200)

        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=400)
