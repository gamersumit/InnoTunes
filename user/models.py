from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length = 50)
    avatar = models.ImageField(upload_to = None, null = True, blank = True)
    email = models.EmailField(unique=True, null = False, blank = False)
    is_artist = models.BooleanField(default = False)
    # password in serializer
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


# extra fields for user 
class Followers(models.Model) :
    artist_id = models.ForeignKey(User, related_name = 'following', on_delete = models.CASCADE)
    user_id = models.ForeignKey(User,related_name = 'follower', on_delete = models.CASCADE)
    
    @staticmethod    
    def get_total_followers(artist):
        return Followers.objects.filter(artist_id = artist).count()  
