from django.contrib.auth.hashers import make_password
import re
from rest_framework.authtoken.models import Token
from cloudinary import uploader
from rest_framework.response import Response
import os
import cloudinary.api
from user.models import User

class UserUtils :

    @staticmethod
    def validate_password(value):
    # valid password : >= 8 char, must contains lower at least 1 char of each 
    # lower(alpha), upper(alpha), (number), (symbols)
    
    # will uncomment later : ---- !>
        # if len(value) < 8:
        #     raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        # if  not re.search("\d", value) :
        #     raise serializers.ValidationError("Password must contains a number 0 to 9")
        
        # if not re.search("[a-z]", value) :
        #     raise serializers.ValidationError("Password must contain a lowercase letter ")
        
        # if not re.search("[A-Z]", value) :
        #     raise serializers.ValidationError("Password must contain a uppercase letter")
        
        # if not re.search(r"[@#$%^&*()\-_+=.]", value):
        #     raise serializers.ValidationError("Password must contain a special character(@,#,$,%,^,&,*,(,),-,_,+,=,.)")

        return make_password(value)    # return hashed password
    

    @staticmethod
    def getUserFromToken(token):
        try :
            token = Token.objects.get(key = token)
            user = token.user
            return user
        
        except Exception as e :
            raise Exception(str(e))
        

class CommonUtils:
    
    @staticmethod
    def UploadMediaToCloud(media, path):
        try : 
            ## song duration
            if path in ['audio', 'colab_audio']:
                upload = uploader.upload_large(media, folder = path, use_filename = True, resource_type = 'video', video_metadata = True)   

                duration = upload['duration']
                return [duration, upload['url']]   
            upload = uploader.upload_large(media, folder = path, use_filename = True)   
            return upload['url']
        
        except Exception as e:
            raise Exception(str(e))

        
    @staticmethod
    def Update_Create(request, fields):
        try:
            for field in fields :
                if field == 'audio': 
                    res = CommonUtils.UploadMediaToCloud(request.data[field], field)
                    request.data['audio'] = res[1]
                    request.data['audio_duration'] = int(res[0])
                elif field == 'colab_audio':
                    res = CommonUtils.UploadMediaToCloud(request.data[field], field)
                    request.data['colab_audio'] = res[1]
                    request.data['audio_duration'] = int(res[0])
                elif request.data.get(field):
                    request.data[field] = CommonUtils.UploadMediaToCloud(request.data[field], field)
                    
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def Serialize(data, serializer_class):
        try:
            serializer = serializer_class(data = data)
            print("Serializer: ", serializer)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response({'message' : 'request successful'}, status = 200)
            
        except Exception as e:
            return Response({'message' : str(e)}, status = 400)

    @staticmethod
    def Delete_Media(request, fields): 
        print("In method::::\n")
        print(request.data)
        print("Fields: ", fields)
        if request.data.get(id):
            print("id: ", request.data.get(id))
            print("song_id: ", request.data.get('song_id'))
            print("user id: ", request.data.get('user_id'))
            try:
                for field in fields:
                    url = request.data.get(field)
                    public_id = cloudinary.utils.cloudinary_url(url)[0]
                    deletion_response = cloudinary.uploader.destroy(public_id)
                    if deletion_response.get('result') == 'ok':
                        print(f'{field} deleted successfully')
                        return Response({'message': f'{field} deleted successfully'})

            except Exception as e:
                return Response({'error': str(e)}, status=400)
