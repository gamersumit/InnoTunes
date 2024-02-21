from django.shortcuts import render
from .serializers import CommentSerializer
from rest_framework.views import APIView
from .models import Comment
from user.models import User
from song.models import Song
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class CreateCommentView(APIView):
    def post(self, request):
        song_id = Song.objects.get(id = 1)
        user_id = User.objects.get(id = 1)
        serializer = CommentSerializer(data = request.data, context = {'song_id': song_id, 'user_id': user_id})
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            print(serializer)
            return Response({'msg': 'Done'}, status = status.HTTP_200_OK)

class UserCommentView(APIView):
    def get(self, request):
        # user = request.user
        user_id = User.objects.get(id = id)
        comments = Comment.objects.filter(user_id = user_id)
        serializer = CommentSerializer(comments, many = True)
        return Response(serializer.data)

class SongCommentView(APIView):
    def get(self, request):
        song_id = Song.objects.get(id = id)
        comments = Comment.objects.get(song_id = song_id)
        serializer = CommentSerializer(comments, many = True)
        return Response(serializer.data)