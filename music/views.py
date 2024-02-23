from rest_framework.views import APIView
from .models import Song, Playlist, SongsInPlaylist
from .serializers import SongSerializer, PlaylistSerializer, SongsInPlaylistSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework import permissions
from utils.utils import UserUtils
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

class SongListAPIView(ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class PlayListViewSet(viewsets.ViewSet):    
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']
    
    def get_queryset(self):
        try:
            token = self.request.headers['Authorization'].split(' ')[1]
            user = UserUtils.getUserFromToken(token)
            self.request.data['user_id'] = user
            return Playlist.objects.filter(user_id = user)
        
        except Exception as e:
            raise Exception(str(e))

class SongsInPlayListViewSet(viewsets.ViewSet):    
    serializer_class = SongsInPlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']
    
    def get_queryset(self):
        try:
            token = self.request.headers['Authorization'].split(' ')[1]
            user = UserUtils.getUserFromToken(token)
            playlist = UserUtils.get()
            Playlist = self.request.data['Playlist_id']
            return SongsInPlaylist.objects.filter(playlist_id = Playlist)
        
        except Exception as e:
            raise Exception(str(e))
        
    def retrieve(self, request, pk=None):
        raise Exception('Reterive Action Not Allowed')