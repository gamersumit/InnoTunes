
from .serializers import ColabSerializer, PostCollabSerializer
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
from rest_framework.parsers import MultiPartParser, FormParser
class PostColabView(generics.CreateAPIView):
    serializer_class = PostCollabSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema( 
    operation_summary= "POST A COLAB", 
    operation_description 
    = 'A INNOTUNE FEATURE: Where User can collaborate with any song',
    responses={200: openapi.Response(
        'Login Successfull', ColabSerializer)}
    ) 
    def post(self, request):
        try:  
            urls = []
            CommonUtils.Update_Create(request, ['audio', 'video', 'colab_picture'], urls)
            request.data['user_id'] = request.user.id
            return CommonUtils.Serialize(request.data, ColabSerializer)
        
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
        
    
    @swagger_auto_schema( 
    operation_summary= "VIEW COLABS", 
    operation_description 
    = 'Get all the collabs for a user or get all the collabs for a song. Just specify your choice in "field" parameter',
    manual_parameters=[
            openapi.Parameter(
                'field',
                openapi.IN_PATH,
                description="Field parameter",
                type=openapi.TYPE_STRING,
                enum=["song", "user"],  # Specify your choices here
            ),
        ]
    ) 
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
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk' 
    

    def get_queryset(self):
        return Colab.objects.filter(user_id=self.request.user.id)
       
    @swagger_auto_schema( 
    operation_summary= "OWN COLLAB DELETION", 
    operation_description 
    = 'A User can delete its own collab and also the song artist can delete the collabs but this api only allows users to delete their own collabs'
    ) 
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)        

class ArtistDeleteColabView(generics.DestroyAPIView):

    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'  
    
    def get_queryset(self):
        try :
            song = Colab.objects.get(id = self.kwargs['pk']).song_id
            if self.request.user != song.artist_id :
                return Colab.objects.none()
        
            return Colab.objects.filter(song_id = song.id)
        
        except :
            return Colab.objects.none()
        
    @swagger_auto_schema( 
    operation_summary= "COLAB DELETION FOR SONG's ARTIST", 
    operation_description 
    = 'A User can delete its own collab and also the song artist can delete the collabs and this api  allows artists to delete collabs on their songs'
    ) 
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)