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

## ye 1st class SongView ni hai updated wale code mai...just for myself
from utils.utils import UserUtils, CommonUtils
import cloudinary.api
# Create your views here.

class SongView(APIView):
    def post(self, request):
        serializer = SongSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            ## getting audio duration
            audio_url = serializer.data['audio']
            audio_info = cloudinary.api.resource(audio_url)
            ## metadata --> duration in the cloudinary
            audio_duration = audio_info.get('duration', None)
            
            ## serializer's instance for making updates
            song_instance = serializer.instance
            song_instance.audio_duration = audio_duration
            song_instance.save()
            return Response({'status' : False, 'message': 'Done'}, status = status.HTTP_200_OK)


class SongView(generics.CreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsArtistOrReadOnly, permissions.IsOwnerOrReadOnly]
    
    def post(self, request):
        try:
            if request.data.get('song_picture'):
                request.data['song_picture'] = CommonUtils.UploadToCloud(request.data['song_picture'], 'song')
            if request.data.get('song_video'):
                request.data['song_video'] = CommonUtils.UploadToCloud(request.data.get('song_video'), 'song')
            if request.data.get('song_audio'):
                request.data['song_audio'] = CommonUtils.UploadToCloud(request.data.get('song_audio'), 'song')    
            else:
                raise Exception("No audio provided")
            
            serializer = self.serializer_class(request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response({'message' : serializer.data}, status = 200)
            
        except Exception as e:
            return Response({'message' : str(e)}, status = 400)
           
            
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
    permission_classes = [permissions.IsOwnerOrReadOnly]
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        try:
            return Playlist.objects.filter(user_id=self.request.data['owner_id'])

        except Exception as e:
            return None
    
    def post(self, request):
        try:
            if request.data.get('playlist_picture'):
                request.data['playlist_picture'] = CommonUtils.UploadImageToCloud(request.data['playlist_picture'], 'playlist')
            
            serializer = self.serializer_class(request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response({'message' : serializer.data}, status = 200)
            
        except Exception as e:
            return Response({'message' : str(e)}, status = 400)
 
 
 # album Cruds(these cruds are not for songs inside album)


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsArtistOrReadOnly, permissions.IsOwnerOrReadOnly]
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        try:
            
            id = self.request.data['artist_id']
            return Album.objects.filter(artist_id = id)
        
        except Exception as e:
            return None
    
    def post(self, request):
        try:
            if request.data.get('album_picture'):
                request.data['album_picture'] = CommonUtils.UploadToCloud(request.data['album_picture'], 'album')
            
            serializer = self.serializer_class(request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response({'message' : serializer.data}, status = 200)
            
        except Exception as e:
            return Response({'message' : str(e)}, status = 400)
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
