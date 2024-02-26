from collections import UserDict
from curses.ascii import SO
from rest_framework.views import APIView
from .models import Song, Playlist, SongsInAlbum, SongsInPlaylist
from .serializers import *
from .permissions import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import viewsets, generics
from rest_framework import permissions
from utils.utils import UserUtils
from user.permissions import *
from music import serializers

# Create your views here.

# <! ---------------- songs views ------------------ !>
# Add a song view


class SongView(generics.CreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsArtistOrReadOnly, IsOwnerOrReadOnly]

# list all songs
class SongListView(ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            field = self.kwargs.get('field', None).title()
            id = self.kwargs.get('id', None)
            if not field:
                model = Song
            elif field == 'Artist':
                model = Song
            elif field == 'Album':
                model = SongsInAlbum
            elif field == 'Playlist':
                model = SongsInPlaylist
            else:
                raise Exception('Invalid Url : /songs/!/!')

            return model.objects.filter(id=id)

        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=200)


# <! ---------------- Playlist views ------------------ !>
#  playlist CRUDS(these cruds are not for songs inside playlist) view
class PlaylistViewSet(viewsets.ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        try:
            return Playlist.objects.filter(user_id=self.request.data['owner_id'])

        except Exception as e:
            return None
 # album Cruds(these cruds are not for songs inside album)


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    permission_classes = [IsArtistOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        try:
            
            id = self.request.data['artist_id']
            return Album.objects.filter(artist_id = id)
        
        except Exception as e:
            return None
# post and delete operations for songs inside a playlist

class AddDeleteSongsFromPlaylistView(generics.GenericAPIView):
    queryset = SongsInPlaylist.objects.all()
    serializer_class = SongsInPlaylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsPlaylistOwner]

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
    permission_classes = [permissions.IsAuthenticated, IsAlbumOwner]

    def post(self):
        try:

            data = {}
            data['song_id'] = self.kwargs.get('song_id')
            data['album_id'] = self.kwargs.get('album_id')

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)

            serializer.save()
            return Response({'status': True, 'message': 'Songs Added to album Successfuly'}, status=200)

        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=400)

    def delete(self):
        try:
            data = {}
            data['album_id'] = self.kwargs.get('album_id')
            data['song_id'] = self.kwargs.get('song_id')

            SongsInAlbum.objects.get(**data).delete()

            return Response({'status': True, 'message': 'Song Removed from album Successfuly'}, status=200)

        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=400)
