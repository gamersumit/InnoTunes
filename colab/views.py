
from .serializers import ColabSerializer
from rest_framework import status, generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user.permissions import *
from utils.utils import  CommonUtils
from user.permissions import *
from .models import Colab
from django.shortcuts import get_object_or_404
# Create your views here.
from music.models import *

from colab import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
    
class ColabView(generics.CreateAPIView):
    serializer_class = ColabSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema( 
    operation_summary= "POST A COLAB", operation_description = 'A INNOTUNE FEATURE: Where User can create/a colab with any song') 
    # responses={200: openapi.Response('Login Successfull', LoginResponseSerializer)})
    def post(self, request):
        try:  
            urls = []
            CommonUtils.Update_Create(request, ['audio', 'video', 'colab_picture'], urls)
            request.data['user_id'] = request.user.id
            return CommonUtils.Serialize(request.data, self.serializer_class)
        
        except Exception as e:
            CommonUtils.delete_media_from_cloudinary(urls)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
   
class GetColabsView(ListAPIView):
    serializer_class = ColabSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            field = self.kwargs.get('field', None)
            id = self.kwargs.get('id')
            if field == 'song':
                return Colab.objects.filter(song_id = id)
            elif field == 'user':
                return Colab.objects.filter(user_id=id)
            else:
                raise Exception('Invalid Url : /colab/!/!')

        except Exception as e:
            return Colab.objects.none()
    
    
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            if self.kwargs['field'] == 'song':
                song = get_object_or_404(Song, id=self.kwargs['id'])
                return Response({'song_info': {'song_name': song.song_name, 'song_id': song.id}, 'results': serializer.data}, status=200)
            else:
                return Response({'colabs': serializer.data}, status=200)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=400)
    
class UserDeleteColabView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsUserOwnerOrReadOnly]
    lookup_field = 'pk' 
    
    def get_queryset(self):
        try:
            return Colab.objects.filter(user_id=self.request.data['user_id'])
        except Exception as e:
            return []        

class ArtistDeleteColabView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsArtistOwnerOrReadOnly]
    lookup_field = 'pk'  
    
    def get_queryset(self):
        if Colab.objects.filter(id = self.kwargs['pk']).exists():
            song = Colab.objects.get(id = self.kwargs['pk']).song_id
            if song.artist_id == self.request.data['artist_id'] :
                return Colab.objects.filter(song_id = song.id)
        return []