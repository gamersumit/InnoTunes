from django.shortcuts import render
from .serializers import ColabSerializer
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from utils.utils import UserUtils, CommonUtils
from .models import Colab
from user.permissions import *
from user.models import User
from collections import defaultdict
# from user.permissions import permissions
# Create your views here.

    
class ColabViewSet(viewsets.ViewSet):
    serializer_class = ColabSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']
    lookup_field = 'pk'
    
    def create(self, request):
        try:
            colab_picture = request.data.get('song_picture', None)
            
            if colab_picture is None:
                user_id = request.data['user_id']
                user = User.objects.get(id = user_id)
                user_avatar = user.avatar
                request.data['song_picture'] = user_avatar
                CommonUtils.Update_Create(request, ['audio', 'video'])
                
            else:
                CommonUtils.Update_Create(request, ['song_picture','audio','video'])
            # print(self.serializer_class)

            serialized_result =  CommonUtils.Serialize(request.data, self.serializer_class)
            print(serialized_result)
            return serialized_result
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
   
class GetColabsView(generics.ListAPIView):
    serializer_class = ColabSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            field = self.kwargs.get('field', None)
            id = self.kwargs.get('id')
            if field == 'song':
                # result = Colab.objects.filter(song_id = id)
                # print(result)
                # self.serializer_class(result, many = True)
                # return result
                return Colab.objects.filter(song_id = id)
            elif field == 'user':
                return Colab.objects.filter(user_id=id)
            else:
                raise Exception('Invalid Url : /colab/!/!')

        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=200)
    
class UserDeleteColabView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]
    lookup_field = 'pk' 
    
    def get_queryset(self):
        return Colab.objects.filter(user_id = self.request.data['user_id'])  

class ArtistDeleteColabView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsArtistOwnerOrReadOnly]
    lookup_field = 'pk'  
    
    def get_queryset(self):
        if Colab.objects.filter(id = self.kwargs['pk']).exists():
            song = Colab.objects.get(id = self.kwargs['pk']).song_id
            if song.artist_id == self.request.data['artist_id'] :
                return Colab.objects.filter(song_id = song.id)
        return []