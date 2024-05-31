from os import stat
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
from user.permissions import IsArtist
from utils.utils import CommonUtils, UserUtils
from user.permissions import *
from music import serializers
import json
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

# <! ---------------- songs views ------------------ !>
# Add a song view


class SongCreateView(generics.CreateAPIView):
    queryset = Song.objects.all()
    serializer_class = PostSongSerializer
    permission_classes = [IsArtist]
    parser_classes = (MultiPartParser, FormParser)
    
    @swagger_auto_schema(tags = ['Song'], 
    operation_summary= "POST SONG",
    operation_description 
        = 'Only Artist are allowed to post songs. This API is to let an artist, realese a song on our app',
    responses={200: openapi.Response( "SONG UPLOADED SUCCESSFULLY",SongSerializer)},
    )
    def post(self, request):
        try:
            urls = []
            CommonUtils.Update_Create(
                request, ['song_picture', 'audio', 'video'], urls) 
            
            request.data['artist_id'] = request.user.id
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
    
    @swagger_auto_schema(tags = ['Song'], 
    operation_summary= "LIST ALL SONGS",
    operation_description 
        = 'RETURNS A PAGINATED LIST OF ALL SONGS IN THE DB. Also User can send (song_name) as query parameter to search specific songs.',
   )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class GuestUserSongListView(ListAPIView):
    serializer_class = SongSerializer
    def get_queryset(self):
       return Song.objects.all()[:10]


    @swagger_auto_schema(tags = ['Song'], 
    operation_summary= "SONGS FOR GUEST USER",
    operation_description 
        = 'RETURNS A LIST OF FEW SPECIFIC SONGS AVAILABLE FOR EVERYONE',
   )       
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# list all songs


class ArtistSongListView(ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Song.objects.filter(artist_id=self.kwargs.get('id'))

    @swagger_auto_schema(tags = ['Song'], 
    operation_summary= "SONGS BY ARTIST",
    operation_description 
        = 'RETURNS A PAGINATED LIST OF ALL SONGS BELONGS TO AN ARTIST',
   )    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class PlaylistSongListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags = ['Song'], 
    operation_summary= "SONGS IN PLAYLIST",
    operation_description 
        = 'RETURNS A PAGINATED LIST OF ALL SONGS INSIDE GIVEN PLAYLIST WITH THE PLAYLIST BRIEF DETAILS',
   )    
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

    @swagger_auto_schema(tags = ['Song'], 
    operation_summary= "LIKED SONGS OF A USER",
    operation_description 
        = 'RETURNS A PAGINATED LIST OF ALL SONGS LIKED BY A USER. ANYONE CAN VIEW ANYONES LIKED SONGS.',
   )    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class AlbumSongListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags = ['Song'], 
    operation_summary= "SONGS INSIDE AN ALBUM",
    operation_description 
        = 'RETURNS A PAGINATED LIST OF ALL SONGS INSIDE GIVEN ALBUM WITH THE ALBUM\'S BRIEF DETAILS',
   )  
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
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'patch', 'delete']
    parser_classes = (MultiPartParser, FormParser)
    
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return PlaylistSerializer
        elif self.action == 'create':
            return PostPlaylistSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return EditPlaylistSerializer
        return PlaylistSerializer


    def get_queryset(self):
        try:
            
            user = self.request.user
            return Playlist.objects.filter(user_id=user.id)

        except Exception as e:
            return Playlist.objects.none()

    @swagger_auto_schema(tags = ['Playlist'], 
    operation_summary= "CREATE A PLAYLIST",
    operation_description 
        = 'USER CAN CREATE A PLAYLIST WITH THIS API. Also they can specify if there playlist should be kept private or public by specifying parameter is_global as True/False respectively.',
    responses={200: openapi.Response('Playlist Created successfully', PlaylistSerializer)},
   )  
    def create(self, request):
        try: 
            urls = []
            CommonUtils.Update_Create(request, ['playlist_picture'], urls)
            request.data['user_id'] = request.user
            serializer = PlaylistSerializer(data = request.data)
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

    @swagger_auto_schema(tags = ['Playlist'], 
    operation_summary= "UPDATE PLAYLIST",
    operation_description 
        = 'WITH THIS API USER CAN EDIT PLAYLIST DETAILS BUT IT DOES NOT TO PERFORM ANY ACTION ON SONGS INSIDE PLAYLIST.',
    responses={200: openapi.Response('Playlist updated successfully', PlaylistSerializer)},
   ) 
    def partial_update(self, request, *args, **kwargs):
        try:
            id = kwargs['pk']
            urls = []
            if not Playlist.objects.filter(id = id).exists():
                raise Exception('Playlist not found')
            
            if not request.data :
                raise Exception('Nothing to be updated')
            
            CommonUtils.Update_Create(request, ['playlist_picture'], urls)
            playlist = Playlist.objects.get(id = id)
            
            request.data['user_id'] = request.user.id
            serializer = PlaylistSerializer(playlist, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'playlist updated successfully'}, status = 200)

        except Exception as e:
            CommonUtils.delete_media_from_cloudinary(urls)
            return Response({'message': str(e)}, status=400)

    @swagger_auto_schema(tags = ['Playlist'], 
    operation_summary= "DELETE A PLAYLIST",
    operation_description 
        = 'WITH THIS USER CAN DELETE A PLAYLIST',
    responses={204: openapi.Response('Playlist Deleted successfully')},
   ) 
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(tags = ['Playlist'], 
    operation_summary= "VIEW PLAYLIST BY ID",
    operation_description 
        = 'WITH THIS USER CAN SEE PLAYLIST DETAILS NOT SONGS INSIDE PLAYLIST',
   ) 
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags = ['Playlist'], 
    operation_summary= "VIEW ALL PLAYLISTS",
    operation_description 
        = 'WITH THIS USER CAN SEE ALL OF THEIR PLAYLISTS DETAILS NOT SONGS INSIDE PLAYLIST',
   ) 
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# album Cruds(these cruds are not for songs inside album)
class AlbumViewSet(viewsets.ModelViewSet):
    permission_classes = permissions.IsAuthenticated
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return AlbumSerializer
        elif self.action == 'create':
            return PostAlbumSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return EditAlbumSerializer
        return AlbumSerializer


    def get_queryset(self):
        try:
            return Album.objects.filter(artist_id=self.request.user.id)

        except Exception as e:
            return Album.objects.none()


    @swagger_auto_schema(tags = ['Album'], 
    operation_summary= "CREATE AN ALBUM",
    operation_description 
        = 'USER CAN CREATE AN ALBUM WITH THIS API',
    responses={200: openapi.Response('Album Created successfully', AlbumSerializer)},
   )  
    def create(self, request):
        try:
            urls = []
            CommonUtils.Update_Create(request, ['album_picture'], urls)
            request.data['artist_id'] = request.user.id
            return CommonUtils.Serialize(request.data, AlbumSerializer)

        except Exception as e:
            CommonUtils.delete_media_from_cloudinary(urls)
            return Response({'message': str(e)}, status=400)

    
    @swagger_auto_schema(tags = ['Album'], 
    operation_summary= "EDIT AN ALBUM",
    operation_description 
        = 'USER CAN EDIT AN ALBUM\'s DETAILS WITH THIS API',
    responses={200: openapi.Response('Album Updated successfully', AlbumSerializer)},
   )
    def update(self, request):
        try:
            urls = []
            CommonUtils.Update_Create(request, ['album_picture'], urls)
            request.data['artist_id'] = request.user.id
            return CommonUtils.Serialize(request.data, AlbumSerializer, partial = True)

        except Exception as e:
            CommonUtils.delete_media_from_cloudinary(urls)
            return Response({'message': str(e)}, status=400)


    @swagger_auto_schema(tags = ['Album'], 
    operation_summary= "DELETE AN ALBUM",
    operation_description 
        = 'USER CAN DELETE AN ALBUM\'s WITH THIS API',
    responses={204: openapi.Response('Album Deleted successfully')},
   )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


    @swagger_auto_schema(tags = ['Album'], 
    operation_summary= "VIEW AN ALBUM",
    operation_description 
        = 'USER CAN VIEW ALBUM\'s DETAILS WITH THIS API',
    responses={200: openapi.Response('Album Deatils', AlbumSerializer)},
   )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    

    @swagger_auto_schema(tags = ['Album'], 
    operation_summary= "VIEW ALL ALBUMS",
    operation_description 
        = 'ARTIST CAN VIEW ALL THEIR ALBUM\'s DETAILS WITH THIS API',
    responses={200: openapi.Response('Album Deatils', AlbumSerializer)},
   )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
# post and delete operations for songs inside a playlist

class AddDeleteSongsFromPlaylistView(generics.GenericAPIView):
    queryset = SongsInPlaylist.objects.all()
    serializer_class = SongsInPlaylistSerializer
    permission_classes = [
        permissions.IsAuthenticated, IsPlaylistOwnerOrReadOnly]


    @swagger_auto_schema(tags = ['Playlist'], 
    operation_summary= "ADD SONGS TO PLAYLIST",
    operation_description 
        = 'USER can add songs to playlist by providing song_id and playlist_id in request_body',
    responses={200: openapi.Response('Song added to playlist successfully', SongsInPlaylistSerializer)},
    )  
    def post(self, request):
        return CommonUtils.Serialize(request.data, self.serializer_class)

    @swagger_auto_schema(tags = ['Playlist'], 
    operation_summary= "DELETE SONGS FROM PLAYLIST",
    operation_description 
        = 'USER can delete songs from playlist by providing song_id and playlist_id in request_body',
    responses={200: openapi.Response('Song deleted from playlist successfully')},
    request_body = SongsInPlaylistSerializer,
    ) 
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
    
    serializer_class = SongsInAlbumSerializer
    permission_classes = [permissions.IsAuthenticated, IsAlbumOwnerOrReadOnly]
    queryset =  SongsInAlbum.objects.all()

    @swagger_auto_schema(tags = ['Album'], 
    operation_summary= "ADD SONG TO ALBUM",
    operation_description 
        = 'Artist can add songs to album by providing song_id and album_id in request_body',
    responses={200: openapi.Response('Song added to album successfully')},
    request_body = SongsInAlbumSerializer,
    )
    def post(self, request):
        return CommonUtils.Serialize(request.data, self.serializer_class)

    @swagger_auto_schema(tags = ['Album'], 
    operation_summary= "DELETE SONG FFROM ALBUM",
    operation_description 
        = 'Artist can delete songs from album by providing song_id and album_id in request_body',
    responses={200: openapi.Response('Song deleted from album successfully')},
    request_body = SongsInAlbumSerializer,
    ) 
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
    serializer_class = EditRecentSongsSeriailizer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = None
    http_method_names = ['put']

    @swagger_auto_schema(tags = ['Recents'], 
    operation_summary= "EDIT RECENTLY PLAYED SONGS",
    operation_description 
        = 'To update the timing of last played and recently played song or if a new song is just played add it to recents.',
    responses={200: openapi.Response('UPDATED RECENTS')},
    )

    def put(self, request):
        try:
            song_id = request.data['song_id']
            request.data['song_id'] = request.user.id
            user_id = request.user.id
            if RecentSongs.objects.filter(song_id=song_id, user_id=user_id).exists():
                recent = RecentSongs.objects.get(
                    song_id=song_id, user_id=user_id)
                recent.last_played_at = timezone.now()
                recent.save()

            else:
                serializer = RecentSongsSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            return Response({'message': 'Updated recents'}, status=200)

        except Exception as e:
            return Response({'message ': str(e)}, status=400)

    # have to implement cron job to remove recents after every 1 hour


class RecentSongsListView(generics.ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        recent_songs = RecentSongs.objects.filter(user_id = user.id).order_by(
            '-last_played_at')[:10]
        recent_songs = [song.song_id for song in recent_songs]
        return recent_songs


    @swagger_auto_schema(tags = ['Recents'], 
    operation_summary= "FETCH RECENTLY PLAYED SONGS",
    operation_description 
        = 'USER CAN VIEW THEIR LATEST 10 RECENTLY PLAYED SONGS',
    responses={200: openapi.Response('Album Deatils', AlbumSerializer)},
   )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class LikedPlaylistListView(generics.ListAPIView):
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        playlist = [playlist.playlist_id for playlist in PlaylistLikes.objects.filter(
            user_id=user.id)]
        return playlist

    @swagger_auto_schema(tags = ['Playlist'], 
    operation_summary= "FETCH ALL LIKED PLAYLISTS",
    operation_description 
        = 'RETURNS A PAGINATED LIST OF ALL THE PLAYLISTS LIKED BY THE USER',
   )  
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class LikedAlbumListView(generics.ListAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    
    def get_queryset(self):
        user = self.request.user
        album = [album.album_id for album in AlbumLikes.objects.filter(
            user_id=user.id)]
        return album
    
    @swagger_auto_schema(tags = ['Album'], 
    operation_summary= "FETCH ALL LIKED ALBUMS",
    operation_description 
        = 'RETURNS A PAGINATED LIST OF ALL THE ALBUMS LIKED BY THE USER',
   )  
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ListUserPlaylistView(generics.ListAPIView):
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Playlist.objects.filter(user_id = self.kwargs['id'])

    @swagger_auto_schema(tags = ['Playlist'], 
    operation_summary= "FETCH ALL PLAYLISTS WITH USER ID",
    operation_description 
        = 'RETURNS A PAGINATED LIST OF ALL THE PLAYLISTS WITH USER\'s ID IN URL',
   )  
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ListUserAndLikedPlaylist(generics.ListAPIView): 
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset =  Playlist.objects.filter(user_id = user.id)   
        queryset.extend([playlist.playlist_id for playlist in PlaylistLikes.objects.filter(
            user_id=user.id)])
        
        return queryset
    
    @swagger_auto_schema(tags = ['Playlist'], 
    operation_summary= "FETCH CURRENT USER'S PLAYLISTS",
    operation_description 
        = 'RETURNS A PAGINATED LIST OF ALL THE PLAYLISTS OF CURRENT USER (LIKED + CREATED)',
   )  
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

        
class GnereListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GnereSerializer
    permission_classes = [permissions.IsAuthenticated]
    

    @swagger_auto_schema(tags = ['Genre'], 
    operation_summary= "FETCH ALL GENERES",
    operation_description 
        = 'RETURNS A PAGINATED LIST OF ALL THE GENRES',
   )  
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
