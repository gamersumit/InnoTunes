from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Album
from .serializers import AlbumSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class AlbumViewSet(viewsets.ViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    
    def create(self, request):
        return Response({'status': True, 'message': 'Success'}, status = status.HTTP_200_OK)        
    
    def list(self, request):
        return Response({'status': True, 'message': 'Success'}, status = status.HTTP_200_OK)
    