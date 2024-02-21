from rest_framework import serializers
from .models import User
from utils.utils import UserUtils

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, min_length = 8, write_only = True)
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'name',
            'is_artist',
        ]
    
    
    
    def validate_password(self, value):
       return UserUtils.validate_password(value)
    


    
   