from django.utils import timezone
from pydoc import plain
from rest_framework.views import APIView
from .models import *
from comment.models import PlaylistLikes, AlbumLikes
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
        try:
            CommonUtils.Update_Create(
                request, ['song_picture', 'audio', 'video'])
            return CommonUtils.Serialize(request.data, SongSerializer)

        except Exception as e:
            return Response({'message': str(e)}, status=400)

# list all songs


class AllSongListView(ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Song.objects.all()

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
            print(queryset)
            playlist = Playlist.objects.get(id=self.kwargs.get('id'))
            print(playlist)
            playlist = PlaylistSerializer(playlist).data
            print(playlist)
            songs = SongSerializer(queryset, many=True).data
            print(songs)
            data = {"playlist": playlist, "songs": songs}
            print(data)
            return Response(data, status=200)

        except Exception as e:
            return Response({'message': str(e)})


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
            return None

    def create(self, request):
        try:
            CommonUtils.Update_Create(request, ['playlist_picture'])
            return CommonUtils.Serialize(request.data, PlaylistSerializer)

        except Exception as e:
            return Response({'message': str(e)}, status=400)

    def update(self, request):
        try:
            CommonUtils.Update_Create(request, ['playlist_picture'])
            return CommonUtils.Serialize(request.data, PlaylistSerializer)

        except Exception as e:
            return Response({'message': str(e)}, status=400)


# album Cruds(these cruds are not for songs inside album)
class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    permission_classes = permissions.IsAuthenticated, IsArtistOwnerOrReadOnly
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        try:

            id = self.request.data['artist_id']
            return Album.objects.filter(artist_id=id)

        except Exception as e:
            return {}

    def create(self, request):
        try:
            CommonUtils.Update_Create(request, ['album_picture'])
            return CommonUtils.Serialize(request.data, AlbumSerializer)

        except Exception as e:
            return Response({'message': str(e)}, status=400)

    def update(self, request):
        try:
            CommonUtils.Update_Create(request, ['album_picture'])
            return CommonUtils.Serialize(request.data, AlbumSerializer)

        except Exception as e:
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
            print(playlist_song)
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
    serializer_class = RecentSongsSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]

    def get_queryset(self):
        recent_songs = RecentSongs.objects.filter().order_by(
            '-last_played_at')[:10]
        return recent_songs


class LikedPlaylistListView(generics.ListAPIView):
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]

    def get_queryset(self):
        token = self.request.headers['Authorization'].split(' ')[1]
        user = UserUtils.getUserFromToken(token)
        playlist = [playlist.playlist_id for playlsit in PlaylistLikes.objects.filter(
            user_id=user.id)]
        return playlist


class LikedAlbumListView(generics.ListAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]

    def get_queryset(self):
        token = self.request.headers['Authorization'].split(' ')[1]
        user = UserUtils.getUserFromToken(token)
        album = [album.album_id for album in AlbumLikes.objects.filter(
            user_id=user.id)]
        return album
