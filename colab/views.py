from django.shortcuts import render
from .serializers import ColabSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from utils.utils import UserUtils, CommonUtils
from .models import Colab
from user.permissions import *
# Create your views here.

    
class ColabViewSet(viewsets.ModelViewSet):
    serializer_class = ColabSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'pk'
    
    def create(self, request):
        try:
            CommonUtils.Update_Create(request, ['colab_picture','colab_audio','colab_video'])
            print(self.serializer_class)

            serialized_result =  CommonUtils.Serialize(request.data, self.serializer_class)
            print(serialized_result)
            return serialized_result
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request):
        try:
            instance = self.get_object()
            
            print("instance: ", instance)
            media_deletion = CommonUtils.Delete_Media(request, ['colab_picture', 'colab_audio', 'colab_view'])
            if media_deletion is not None:
                print(media_deletion)
                # return media_deletion
            self.perform_destroy(instance)
            print("instance after deletion: ", instance)
            # request.delete()
            return Response({'message':'Colab deleted successfully'})
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk = None):
        try:
            
            ## as request body
            # song_id = request.data.get('song_id')
            # user_id = request.data.get('user_id')

            ## as dynamic url
            # song_id = self.kwargs.get('song_id')
            # user_id = self.kwargs.get('user_id')
            
            ## as query params
            song_id = request.query_params.get('song_id')
            user_id = request.query_params.get('user_id')

            if song_id:
                queryset = Colab.objects.filter(song_id=song_id)
            elif user_id:
                queryset = Colab.objects.filter(user_id=user_id)
            else:
                return Response({'message':"Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
   