from django.shortcuts import render
from .serializers import CommentSerializer
from rest_framework.views import APIView
from .models import Comment
from user.models import User
from music.models import Song
from rest_framework.response import Response
from rest_framework import status
from utils.utils import UserUtils
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # song_id = Song.objects.get(id = 1)    ## for testing
        # user_id = User.objects.get(id = 1)
        try:
            song_id = self.request.data.get('song_id')
            token = self.request.headers['Authorization'].split(' ')[1]
            user = UserUtils.getUserFromToken(token)    # instance of User model
            user_id = user.id
        except KeyError:
            return Response({'error': 'Invalid request data. Please provide song_id and Authorization token.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise Exception(str(e))
        
        serializer = CommentSerializer(data = request.data, context = {'song_id': song_id, 'user_id': user_id})
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            print(serializer)
            return Response({'msg': 'Done'}, status = status.HTTP_200_OK)

class UserCommentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # user = request.user
        try:
            token = self.request.headers['Authorization'].split(' ')[1]
            user = UserUtils.getUserFromToken(token)    # instance of User model
            user_id = user.id
        except Exception as e:
            raise Exception(str(e))
        # user_id = User.objects.get(id = id)   ## for testing
        comments = Comment.objects.filter(user_id = user_id)
        serializer = CommentSerializer(comments, many = True)
        return Response(serializer.data)

class SongCommentView(APIView):
    def get(self, request):
        # song_id = Song.objects.get(id = id)
        song_id = self.request.data.get('song_id')
        if not song_id:     ## error handling
                return Response({'status': False, 'message': 'Please provide a song_id'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            comments = Comment.objects.filter(song_id = song_id)
            
            if not comments:    ## no comments for particular song
                return Response({'status': False, 'message': 'No comments for the given song_id'}, status= status.HTTP_404_NOT_FOUND)
            
            serializer = CommentSerializer(comments, many = True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        
        