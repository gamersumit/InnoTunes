import resource
from django.contrib.auth.hashers import make_password
import random
from rest_framework.authtoken.models import Token
from cloudinary import uploader
from rest_framework.response import Response
import os
import requests
from user.models import User
import cloudinary
import cloudinary.api
import logging 
from  rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
import re


logger = logging.getLogger( __name__ )

class UserUtils :

    @staticmethod
    def validate_password(value):
    # valid password : >= 8 char, must contains lower at least 1 char of each 
    # lower(alpha), upper(alpha), (number), (symbols)
    
    # will uncomment later : ---- !>
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        if  not re.search("\d", value) :
            raise serializers.ValidationError("Password must contains a number 0 to 9")
        
        if not re.search("[a-z]", value) :
            raise serializers.ValidationError("Password must contain a lowercase letter ")
        
        if not re.search("[A-Z]", value) :
            raise serializers.ValidationError("Password must contain a uppercase letter")
        
        if not re.search(r"[@#$%^&*()\-_+=.]", value):
            raise serializers.ValidationError("Password must contain a special character(@,#,$,%,^,&,*,(,),-,_,+,=,.)")

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
    def UploadMediaToCloud(media, path, urls):
        try : 
            path = f'public/{path}'
            ## song duration
            if path == 'public/audio':
                upload = uploader.upload_large(media, folder = path, use_filename = True, resource_type = 'video', video_metadata = True)   
                duration = upload['duration']
                return [duration, upload['url']]   
            upload = uploader.upload_large(media, folder = path, use_filename = True)   
            urls.append(upload['secure_url'])
            return upload['secure_url']
        
        except Exception as e:
            raise Exception(str(e))
      
    @staticmethod
    def Update_Create(request, fields, urls):
        try:
            for field in fields :
                
                if field == 'audio' : 
                    res = CommonUtils.UploadMediaToCloud(request.data[field], field, urls)
                    request.data['audio'] = res[1]
                    request.data['audio_duration'] = int(res[0])
                elif request.data.get(field):
                    request.data[field] = CommonUtils.UploadMediaToCloud(request.data[field], field, urls)
                    
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
            instance = serializer.save()

            return Response({'message' : 'request successful', 'id' : instance.id}, status = 200)
            
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
              
    @staticmethod
    def delete_media_from_cloudinary(urls):
        try :
            logger.info(urls)
            public_ids = [url[url.index('public/'):] for url in urls]
            response = cloudinary.api.delete_resources(public_ids, resource_type = 'raw')
             
        except Exception as e:
            pass
    
    @staticmethod
    def otp_generator():
        otp = random.randint(100001, 999999)
        return otp
    

class Mail:
    
    def __init__(self, subject, body, emails):
        self.subject = subject
        self.body = body
        self.emails = emails
    
    
    def send(self):
        send_mail(
            self.subject, 
            self.body,
            settings.EMAIL_HOST_USER,
            self.emails,
            fail_silently=False)
        

