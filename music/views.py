from django.utils import timezone
from pydoc import plain
from rest_framework.views import APIView
from .models import *
from comment.models import PlaylistLikes, AlbumLikes, SongLikes
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
import json



# Create your views here.

# <! ---------------- songs views ------------------ !>
# Add a song view


class SongCreateView(generics.CreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    # permission_classes = [permissions.IsAuthenticated, IsArtistOwnerOrReadOnly]

    def post(self, request):
        try:
            urls = []
            CommonUtils.Update_Create(
                request, ['song_picture', 'audio', 'video'], urls) 
            return CommonUtils.Serialize(request.data, SongSerializer)

        except Exception as e:
            CommonUtils.delete_media_from_cloudinary(urls)
            return Response({'message': str(e)}, status=400)

# list all songs


class AllSongListView(ListAPIView):
    serializer_class = SongSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        try:
            queryset = Song.objects.all()
            song_name = self.request.query_params.get('song_name', None)
            if song_name:
                queryset = queryset.filter(song_name__icontains=song_name)
            return queryset
        except Exception as e:
            return Song.objects.none()

class GuestUserSongListView(ListAPIView):
    serializer_class = SongSerializer
    def get_queryset(self):
        try:
            queryset = Song.objects.all()[:10]
            return queryset
        except Exception as e:
            return Song.objects.none()

# list all songs


class ArtistSongListView(ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Song.objects.filter(artist_id=self.kwargs.get('id'))


class PlaylistSongListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, **kwargs):
        try:
            queryset = [song.song_id for song in SongsInPlaylist.objects.filter(
                playlist_id=self.kwargs.get('id'))]
            playlist = Playlist.objects.get(id=self.kwargs.get('id'))
            playlist = PlaylistSerializer(playlist).data  
            songs = SongSerializer(queryset, many=True).data   
            data = {"playlist": playlist, "songs": songs}   
            return Response(data, status=200)

        except Exception as e:
            return Response({'message': str(e)})
        
class LikedSongsListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SongSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['id']
        songs = [song.song_id for song in SongLikes.objects.filter(
            user_id=user_id)]
        return songs


class AlbumSongListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, **kwargs):
        try:
            queryset = [song.song_id for song in SongsInAlbum.objects.filter(
                album_id=self.kwargs.get('id'))]
            album = Album.objects.get(id=self.kwargs.get('id'))
            album = AlbumSerializer(album).data
            songs = SongSerializer(queryset, many=True).data
            data = {"album": album, "songs": songs}
            return Response(data, status=200)

        except Exception as e:
            return Response({'message': str(e)})


# <! ---------------- Playlist views ------------------ !>
#  playlist CRUDS(these cruds are not for songs inside playlist) view
class PlaylistViewSet(viewsets.ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        try:
            token = self.request.headers['Authorization'].split(' ')[1]
            user = UserUtils.getUserFromToken(token)
            return Playlist.objects.filter(user_id=user.id)

        except Exception as e:
            return []

    def create(self, request):
        try: 
            urls = []
            CommonUtils.Update_Create(request, ['playlist_picture'], urls)
            serializer = self.serializer_class(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            playlist_id = data['id']
            songs = json.loads(request.data.get('songs', None))
            if songs :
                for song in  songs :
                    temp = {'playlist_id' : playlist_id, 'song_id' : int(song)}
                    serial = SongsInPlaylistSerializer(data = temp)
                    serial.is_valid(raise_exception=True)
                    serial.save()
                    
            return Response({'message': {'id' : playlist_id}}, status = 200)
        except Exception as e:
            CommonUtils.delete_media_from_cloudinary(urls)
            return Response({'message': str(e)}, status=400)

    def update(self, request):
        try:
            urls = []
            CommonUtils.Update_Create(request, ['playlist_picture'], urls)
            return CommonUtils.Serialize(request.data, PlaylistSerializer)

        except Exception as e:
            CommonUtils.delete_media_from_cloudinary(urls)
            return Response({'message': str(e)}, status=400)


# album Cruds(these cruds are not for songs inside album)
class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    # permission_classes = permissions.IsAuthenticated, IsArtistOwnerOrReadOnly
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        try:
            id = self.request.data['artist_id']
            return Album.objects.filter(artist_id=id)

        except Exception as e:
            return []

    def create(self, request):
        try:
            urls = []
            CommonUtils.Update_Create(request, ['album_picture'], urls)
            return CommonUtils.Serialize(request.data, AlbumSerializer)

        except Exception as e:
            CommonUtils.delete_media_from_cloudinary(urls)
            return Response({'message': str(e)}, status=400)

    def update(self, request):
        try:
            urls = []
            CommonUtils.Update_Create(request, ['album_picture'], urls)
            return CommonUtils.Serialize(request.data, AlbumSerializer)

        except Exception as e:
            CommonUtils.delete_media_from_cloudinary(urls)
            return Response({'message': str(e)}, status=400)


# post and delete operations for songs inside a playlist

class AddDeleteSongsFromPlaylistView(generics.GenericAPIView):
    queryset = SongsInPlaylist.objects.all()
    serializer_class = SongsInPlaylistSerializer
    permission_classes = [
        permissions.IsAuthenticated, IsPlaylistOwnerOrReadOnly]

    def post(self, request):
        return CommonUtils.Serialize(request.data, self.serializer_class)

    def delete(self, request):
        try:
            playlist_id = request.data['playlist_id']
            song_id = request.data['song_id']
            playlist_song = SongsInPlaylist.objects.get(
                playlist_id=playlist_id, song_id=song_id)
            if playlist_song:
                playlist_song.delete()

            else:
                raise Exception(
                    "Given playlist and song combination does'nt exist")

            return Response({'status': True, 'message': 'Song Removed from Playlist Successfuly'}, status=200)

        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=400)


# post and delete operations for songs inside a album
class AddDeleteSongsFromAlbumView(generics.GenericAPIView):
    queryset = SongsInAlbum.objects.all()
    serializer_class = SongsInAlbumSerializer
    permission_classes = [permissions.IsAuthenticated, IsAlbumOwnerOrReadOnly]

    def post(self, request):
        return CommonUtils.Serialize(request.data, self.serializer_class)

    def delete(self, request):
        try:
            album_id = request.data['album_id']
            song_id = request.data['song_id']
            album_song = SongsInAlbum.objects.get(
                album_id=album_id, song_id=song_id)
            if album_song:
                album_song.delete()
            else:
                raise Exception(
                    "Givem album and song combination does'nt exist")
            return Response({'status': True, 'message': 'Song Removed from album Successfuly'}, status=200)

        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=400)


class AddToRecentsView(generics.UpdateAPIView):
    queryset = RecentSongs.objects.all()
    serializer_class = RecentSongsSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]
    lookup_field = None

    def put(self, request):
        try:
            song_id = request.data['song_id']
            user_id = request.data['user_id']
            if RecentSongs.objects.filter(song_id=song_id, user_id=user_id).exists():
                recent = RecentSongs.objects.get(
                    song_id=song_id, user_id=user_id)
                recent.last_played_at = timezone.now()
                recent.save()

            else:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            return Response({'message': 'Updated recents'}, status=200)

        except Exception as e:
            return Response({'message ': str(e)}, status=400)

    # have to implement cron job to remove recents after every 1 hour


class RecentSongsListView(generics.ListCreateAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = UserUtils.getUserFromToken(self.request.headers['Authorization'].split(' ')[1])
        recent_songs = RecentSongs.objects.filter(user_id = user.id).order_by(
            '-last_played_at')[:10]
        recent_songs = [song.song_id for song in recent_songs]
        return recent_songs


class LikedPlaylistListView(generics.ListAPIView):
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]

    def get_queryset(self):
        token = self.request.headers['Authorization'].split(' ')[1]
        user = UserUtils.getUserFromToken(token)
        playlist = [playlist.playlist_id for playlist in PlaylistLikes.objects.filter(
            user_id=user.id)]
        return playlist


class LikedAlbumListView(generics.ListAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        token = self.request.headers['Authorization'].split(' ')[1]
        user = UserUtils.getUserFromToken(token)
        album = [album.album_id for album in AlbumLikes.objects.filter(
            user_id=user.id)]
        return album


class ListUserPlaylistView(generics.ListAPIView):
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Playlist.objects.filter(user_id = self.kwargs['id'])

class ListUserAndLikedPlaylist(generics.ListAPIView): 
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        token = self.request.headers['Authorization'].split(' ')[1]
        user = UserUtils.getUserFromToken(token)
        queryset =  Playlist.objects.filter(user_id = user.id)   
        queryset.extend([playlist.playlist_id for playlist in PlaylistLikes.objects.filter(
            user_id=user.id)])
        
        return queryset
        
class GnereListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GnereSerializer
    permission_classes = [permissions.IsAuthenticated]
    

