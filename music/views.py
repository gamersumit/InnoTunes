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
import random


# Create your views here.

# <! ---------------- songs views ------------------ !>
# Add a song view


class SongCreateView(generics.CreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    # permission_classes = [permissions.IsAuthenticated, IsArtistOwnerOrReadOnly]

    def post(self, request):
        print("here")
        try:
            urls = []
            # CommonUtils.Update_urls(request, ['song_picture','audio','video'],urls)
            CommonUtils.Update_Create(
                request, ['song_picture', 'audio', 'video'], urls)
            serialized_data = CommonUtils.Serialize(request.data, SongSerializer)
            return Response(serialized_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            CommonUtils.delete_media_from_cloudinary(urls)
            return Response({'message': str(e)}, status=400)
    

    def put(self, request):
        urls = []
        try:
            print("there")
            song_id = request.data.get('id')
            # print("request: ", request.data)
            instance = Song.objects.get(id = song_id)
            print("instance: ", instance)
            if 'song_picture' in request.data:
                CommonUtils.Update_Create(
                    request, ['song_picture'], urls)
                print("here")
            if 'audio' in request.data:
                CommonUtils.Update_Create(
                    request, ['audio'], urls)
                print("here")
            if 'video' in request.data:
                CommonUtils.Update_Create(
                    request, ['audio'], urls)
                print("here")
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            print("yo")
            serializer.is_valid(raise_exception=True)
            # if 'audio' not in request.data:
            #     song = Song.objects.get(id = request.data['id'])
            #     print("song: ", song)
            #     print("audio: ", song.audio)
            #     serializer.validated_data['audio'] = song.audio
            #     serializer.save()
            serializer.save()
            print("done")
            return Response(serializer.data, status= status.HTTP_202_ACCEPTED)
            # print("here")
        except Exception as e:
            CommonUtils.delete_media_from_cloudinary(urls)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            

# list all songs

from rest_framework import viewsets
from .models import Song
from .serializers import SongSerializer


class AllSongListView(ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        try:
            queryset = Song.objects.all()
            song_name = self.request.query_params.get('song_name', None)
            print("song_name: ", song_name)
            genre = self.request.query_params.get('genre', None)
            print("genre: ", genre)
            if song_name:
                print("neh1")
                queryset = queryset.filter(song_name__icontains=song_name)
            elif genre:
                print("neh")
                queryset = queryset.filter(genre__genre__icontains = genre)
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
    # permission_classes = [permissions.IsAuthenticated]

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
    # permission_classes = [permissions.IsAuthenticated]

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
    # permission_classes = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete', 'patch']

    def get_queryset(self):
        try:
            token = self.request.headers['Authorization'].split(' ')[1]
            user = UserUtils.getUserFromToken(token)
            return Playlist.objects.filter(user_id=user.id)

        except Exception as e:
            return []

    def create(self, request):
        print("in create")
        print("request: ", request.data)
        try: 
            urls = []
            CommonUtils.Update_Create(request, ['playlist_picture'], urls)
            serializer = self.serializer_class(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            playlist_id = data['id']
            print("hey1")
            if request.data.get('songs'):
                songs = json.loads(request.data.get('songs', None))
                if songs :
                    for song in  songs :
                        temp = {'playlist_id' : playlist_id, 'song_id' : int(song)}
                        serial = SongsInPlaylistSerializer(data = temp)
                        serial.is_valid(raise_exception=True)
                        print("hey")
                        serial.save()       
            return Response({'message': {'id' : playlist_id}}, status = status.HTTP_201_CREATED)
        except Exception as e:
            print("hey")
            # CommonUtils.delete_media_from_cloudinary(urls)
            print("message", str(e))
            return Response({'message': str(e)}, status=400)

    def partial_update(self, request, pk = None):
        try:
            urls = []
            CommonUtils.Update_Create(request, ['playlist_picture'], urls)
            playlist = Playlist.objects.get(id = pk)
            serializer = self.get_serializer(playlist, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({"message": "Playlist Updated Successfully", "status": status.HTTP_202_ACCEPTED})
        except Exception as e:
            CommonUtils.delete_media_from_cloudinary(urls)
            print("here")
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

    def partial_update(self, request):
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
    # permission_classes = [
    #     permissions.IsAuthenticated, IsPlaylistOwnerOrReadOnly]

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
    # permission_classes = [permissions.IsAuthenticated, IsAlbumOwnerOrReadOnly]

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
    

    
class RecentGenreListView(generics.ListCreateAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = UserUtils.getUserFromToken(self.request.headers['Authorization'].split(' ')[1])
        recent_songs = RecentSongs.objects.filter(user_id = user.id).order_by(
            '-last_played_at').values_list('song_id', flat = True)[:10]
        print(recent_songs)
        # recent_songs = [song.song_id for song in recent_songs]
        print(user)
        # print(recent_songs)
        if len(Song.objects.filter(id__in = recent_songs).values_list('genre', flat = True).distinct()) > 3:
            recent_songs_genres = Song.objects.filter(id__in = recent_songs).values_list('genre', flat = True).distinct()[:3]
        else:
            recent_songs_genres = Song.objects.filter(id__in = recent_songs).values_list('genre', flat = True).distinct()        
        result = []
        for genres in recent_songs_genres:
            song_in_genre = Song.objects.filter(genre = genres)
            if song_in_genre.exists():
                result.append(random.choice(song_in_genre))     ## random song
                # random_song = song_in_genre.order_by('?').first()
                # result.append(random_song)
            print(result)
        return result

class GlobalPlaylistAPIView(APIView):
    serializer_class = GlobalPlaylistSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):        ## for me
        try:
            # token = request.headers['Authorization'].split(' ')[1]
            # token_user = UserUtils.getUserFromToken(token)
            # if token_user.is_artist:
            urls = []
            CommonUtils.Update_Create(request, ['playlist_picture'], urls)
            print("heylo")
            serializer = self.serializer_class(data = request.data)
            serializer.is_valid(raise_exception=True)
            user_id = request.data.get('user_id')
            user = User.objects.get(pk = user_id)
            # request.data['user_id'] = user
            serializer.validated_data['user_id'] = user
            print('heylo')
            serializer.save()
            print("heylo")
            # return serializer
            return Response({'data': serializer.data}, status = status.HTTP_201_CREATED)                
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=400)
    
    def get(self, request, pk = None):
        queryset = Playlist.objects.filter(is_global = True)  
        # if request.data:
        #     queryset = Playlist.objects.get
        serializer = self.serializer_class(queryset, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
class GenreFilterAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        random_genres = Genre.objects.order_by('?').distinct()[:3]
    
        data = []
        for genre in random_genres:
            genre_data = {}
            genre_serializer = GenreSerializer(genre)
            genre_data['genre'] = genre_serializer.data
            
            songs = Song.objects.filter(genre=genre)[:5]  
            song_data = []
            
            for song in songs:
                song_serializer = SongSerializer(song)
                song_data.append(song_serializer.data)
            
            genre_data['songs'] = song_data 
            data.append(genre_data)
        
        return Response(data)

# class GenreDetailsAPI(APIView):
#     def get(self, request):
#         genre = request.data.get('genre')
        
