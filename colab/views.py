from django.shortcuts import render
from .serializers import ColabSerializer
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from utils.utils import UserUtils, CommonUtils
from .models import Colab
from user.permissions import *
from user.models import User
from collections import defaultdict
# Create your views here.

    
class ColabViewSet(viewsets.ViewSet):
    serializer_class = ColabSerializer
    # permission_classes = [permissions.IsAuthenticated]
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
    
   
   
class GetColabsView(ListAPIView):
    serializer_class = ColabSerializer
    # permission_classes = [permissions.IsAuthenticated]

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
   

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     data = defaultdict(list)
    #     # data = defaultdict(dict)
        
    #     for colab in queryset:
    #         user_id = colab.user_id_id  # Assuming user_id is ForeignKey
    #         data[user_id].append({
    #             'id': colab.id,
    #             'song_description': colab.song_description,
    #             'created_at': colab.created_at,
    #             # 'genre': colab.genre,
    #             # 'credits': colab.credits,
    #             'audio_duration': colab.audio_duration,
    #             'audio': colab.audio,
    #             'video': colab.video,
    #             'song_picture': colab.song_picture,
                
    #         })

    #     result = [{user_id: colabs} for user_id, colabs in data.items()]
    #     return Response(result)

  
    
class DeleteColabView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Colab.objects.get(pk=pk)
        except Colab.DoesNotExist:
            raise Response({'message': 'Colab not found'}, status=status.HTTP_404_NOT_FOUND)
                
    def delete(self, request, **kwargs):
        print('aaye')
        try:
            print('noii')
            field = kwargs.get('field')
            id = kwargs.get('id')
            print('one')
            if field == 'song':
                print('five')
                # print("Data to be sent: ", Colab.objects.filter(song_id=id))
                
                media_deletion = CommonUtils.Delete_Media(request, ['colab_picture', 'colab_audio', 'colab_video'])
                print("Deletion called\n")
                if media_deletion is not None:
                    print('two')
                    print(media_deletion)
                
                Colab.objects.filter(song_id=id).delete()
                print('four')
            elif field == 'user':
                Colab.objects.filter(user_id=id).delete()
                # media_deletion = CommonUtils.Delete_Media(request, ['colab_picture', 'colab_audio', 'colab_view'])
                # if media_deletion is not None:
                #     print(media_deletion)
            else:
                # media_deletion = CommonUtils.Delete_Media(request, ['colab_picture', 'colab_audio', 'colab_view'])
                # if media_deletion is not None:
                #     print(media_deletion)
                
                field1 = kwargs.get('field1')
                field2 = kwargs.get('field2')
                id1 = kwargs.get('id1')
                id2 = kwargs.get('id2')
                if field1 == 'song' and field2 == 'user':
                    Colab.objects.filter(song_id=id1, user_id=id2).delete()
                else:
                    raise Exception('Invalid field format')
            return Response({'message': 'Colabs deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
       