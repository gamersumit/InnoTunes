from django.contrib.auth.hashers import make_password
import re
from rest_framework.authtoken.models import Token
from cloudinary import uploader
from rest_framework.response import Response
import os
import cloudinary.api

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
            upload = uploader.upload_large(media, folder = path, use_filename = True)   
        
            ## song duration
            if path == 'audio':
                duration = upload['duration']
                return [duration, upload['url']]   
            return upload['url']
        
        except Exception as e:
            raise Exception(str(e))
    
    # @staticmethod
    # def CloudinaryAudioDuration(audio_url):
    #     try :
    #         audio_info = cloudinary.api.resource(audio_url)
    #         ## metadata --> duration in the cloudinary
    #         return audio_info.get('duration', None)
    #     except :
    #         return None
        
    @staticmethod
    def Update_Create(request, fields):
        try:
            for field in fields :
                
                if field == 'audio' : 
                        
                    res = CommonUtils.UploadMediaToCloud(request.data[field], field)
                    request.data['audio'] = res[1]
                    request.data['audio_duration'] = res[0]
                
                if request.data.get(field):
                    request.data[field] = CommonUtils.UploadMediaToCloud(request.data[field], path)
                    
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def Serialize(data, serializer_class):
        try:
            serializer = serializer_class(data = data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response({'message' : serializer.data}, status = 200)
            
        except Exception as e:
            return Response({'message' : str(e)}, status = 400)