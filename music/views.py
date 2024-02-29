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
class AllSongListView(ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Song.objects.all()

class PlaylistSongListView(ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class AlbumSongListView(ListAPIView):

    def get(self, request):
        try :
            queryset = SongsInAlbum.objects.filter(album_id = self.kwargs.get('id'))
            data = SongSerializer(queryset, many = True).data
            print(data, "########")
            album = Album.object.get(id = self.kwargs.get('id'))
            data.update(AlbumSerializer(album).data)
            return Response({'message' : data}, status = 200)
        
        except Exception as e:
            return Response({'message' : str(e)})
        
        
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

    def post(self, request):
            return CommonUtils.Serialize(request.data, self.serializer_class)

    def delete(self, request):
        try:
            data = {}
            data['playlist_id'] = request.data['playlist_id']
            data['song_id'] = request.data['song_id']

            playlist_song = SongsInPlaylist.objects.get(**data).delete()
            
            if playlist_song:
                playlist_song.delete()
                
            else :
                raise Exception("Givem playlist and song combination does'nt exist")

            return Response({'status': True, 'message': 'Song Removed from Playlist Successfuly'}, status=200)

        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=400)


# post and delete operations for songs inside a album
class AddDeleteSongsFromAlbumView(generics.GenericAPIView):
    queryset = SongsInAlbum.objects.all()
    serializer_class = SongsInAlbumSerializer
    # permission_classes = [permissions.IsAuthenticated, IsAlbumOwnerOrReadOnly]

    def post(self, request):
        return CommonUtils.Serialize(request.data, self.serializer_class)

    def delete(self, request):
        try:
            data = {}
            data['album_id'] = request.data['album_id']
            data['song_id'] = request.data['song_id']

            album_song = SongsInAlbum.objects.get(**data)
            if album_song:
                album_song.delete()
            else :
                raise Exception("Givem album and song combination does'nt exist")
            return Response({'status': True, 'message': 'Song Removed from album Successfuly'}, status=200)

        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=400)
