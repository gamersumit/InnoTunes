from django.shortcuts import render
from rest_framework.views import APIView
from .models import Song
from .serializers import SongSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
# Create your views here.

class SongView(APIView):
    def post(self, request):
        serializer = SongSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Done'}, status = status.HTTP_200_OK)

class SongListAPIView(ListAPIView):
    queryset = SongSerializer.objects.all()
    serializer_class = SongSerializer
    