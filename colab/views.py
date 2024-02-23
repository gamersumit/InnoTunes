from django.shortcuts import render
from .serializers import ColabSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from utils.utils import UserUtils
from .models import Colab
# Create your views here.

class UserColabListViewSet(viewsets.ViewSet):
    serializer_class = ColabSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    # http_method_names = ['get', 'post', 'put', 'delete']
    
    def get_queryset(self):
        if self.action in ['list', 'destroy', 'retrieve']:        
            try:
                song_id = self.request.get('song_id')
                token = self.request.headers['Authorization'].split(' ')[1]
                user = UserUtils.getUserFromToken(token)    # instance of User model
                user_id = user.id
                # self.request.data['user_id'] = user
            
                if song_id and not user_id:
                    return Colab.objects.filter(song_id = song_id)
                elif not song_id and user_id:
                    return Colab.objects.filter(user_id = user_id)
        
            except Exception as e:
                raise Exception(str(e))
            
        else:
            try:
                token = self.request.headers['Authorization'].split(' ')[1]
                user = UserUtils.getUserFromToken(token)    # instance of User model
                user_id = user.id
                return Colab.objects.filter(user_id = user_id)
            
            except Exception as e:
                raise Exception(str(e))
    
    # def create(self, request):
    #     queryset = self.get_queryset()
    #     # serializer = ColabSerializer(queryset)
    #     return Response({'message': 'Colab request received'}, status = status.HTTP_201_CREATED)
    
    # def retrieve(self, request, pk=None):
    #     queryset = self.get_queryset()
    #     serializer = ColabSerializer(queryset)
    #     return Response(serializer.data, {'message': 'Retrieve request received'}, status = status.HTTP_200_OK)
        
    # def update(self, request, pk=None):
    #     queryset = self.get_queryset()
    #     # serializer = ColabSerializer(queryset)
    #     return Response({'message': 'Put request received'}, status = status.HTTP_200_OK)
    
    # def partial_update(self, request, pk=None):
    #     queryset = self.get_queryset()
    #     return Response({'message': 'PATCH request received for object with pk={}'.format(pk)})
    
    # def destroy(self, request, pk=None):
    #     queryset = self.get_queryset()
    #     return Response({'message': 'DELETE request received for object with pk={}'.format(pk)})
    
    # def list(self, request):
    #     queryset = self.get_queryset()  # Use the custom queryset
    #     serializer = self.serializer_class(queryset, many=True)
    #     return Response(serializer.data)
        