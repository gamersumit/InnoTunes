from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length = 50)
    avatar = models.ImageField(upload_to = None, null = True, blank = True)
    email = models.EmailField(unique=True, null = False, blank = False)
    isArtist = models.BooleanField(default = False)
    # password in serializer
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

