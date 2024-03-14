from django.contrib.auth.hashers import make_password
import re
from rest_framework.authtoken.models import Token
from cloudinary import uploader
from rest_framework.response import Response
import os
import requests
from user.models import User
import cloudinary
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
    def UploadToCloud(media, path):
        try : 
            ## song duration
            if path == 'audio':
                upload = uploader.upload_large(media, folder = path, use_filename = True, resource_type = 'video', video_metadata = True)   

                duration = upload['duration']
                return [duration, upload['url']]   
            upload = uploader.upload_large(media, folder = path, use_filename = True)   
            return upload['url']
            
            return upload['url']
            
        except Exception as e:
            return Response(str(e))

    @staticmethod
    def Update_Create(request, fields):
        try:
            for field in fields:
                print("Field: ", field)
                if request.data.get(field):
                    
                    print(request.data[field])
                    if field == 'song_audio':
                        result = CommonUtils.UploadToCloud(request.data[field], field)
                        request.data['song_duration'] = result[0]
                        print("Duration: ", result[0])
                        request.data[field] = result[1]
                        print("song url: ", result[1])
                        
                    else:
                        request.data[field] = CommonUtils.UploadToCloud(request.data[field], field)
                        print("other urls: ", request.data[field])
                                      
        except Exception as e:
            raise Exception(str(e))

    @staticmethod
    def Delete_Media(request, fields): 
        if request.data.get(id):
            print("id: ", request.data.get(id))
            try:
                for field in fields:
                    url = request.data.get(field)
                    public_id = cloudinary.utils.cloudinary_url(url)[0]
                    deletion_response = cloudinary.uploader.destroy(public_id)
                    if deletion_response.get('result') == 'ok':
                        return Response({'message': f'{field} deleted successfully'})
                    else:
                        return Response({'error': f'Failed to delete {field}'}, status=400)
            except Exception as e:
                return Response({'error': str(e)}, status=400)
    
    @staticmethod
    def Serialize(data, serializer_class):
        try:
            serializer = serializer_class(data = data)
            print(serializer)
            
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response({'message' : serializer.data}, status = 200)
            
        except Exception as e:
            return Response({'message' : str(e)}, status = 400)

class GoogleUtils:
    
    @staticmethod
    def GetAccountInfo(request):
        try:
            code = request.GET.get('code')
            if code:
                client_id = os.getenv('CLIENT_ID')
                client_secret = os.getenv('CLIENT_SECRET')
                redirect_uri = 'http://localhost:8000/accounts/google/login/callback/'
                token_endpoint = 'https://oauth2.googleapis.com/token'
                # token_endpoint = 'https://accounts.google.com/o/oauth2/token'
        
                payload = {
                    'code': code,
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'redirect_uri': redirect_uri,
                    'grant_type': 'authorization_code'
                }
                print("Payload: ", payload)
                print("code:", code)
                
                response = requests.post(token_endpoint, data = payload)
                print("Response:", response)
                print("response: ", response.json())
                access_token = response.json().get('access_token')
                
                userinfo_endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'
                
                headers = {'Authorization': f'Bearer {access_token}'}
                userinfo_response = requests.get(userinfo_endpoint, headers=headers)
                print("userinfo_response: ", userinfo_response)
                
                userinfo = userinfo_response.json()
                print("userinfo: ", userinfo)

                # Check if user with the fetched email exists
                user = User.objects.filter(email=userinfo.get('email'))
                print("user: ", user)
                return userinfo
        except Exception as e:
            return Response({'message': str(e)})