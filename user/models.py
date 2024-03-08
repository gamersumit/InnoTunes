from django.db import models
from django.contrib.auth.models import AbstractUser




# Create your models here.
class User(AbstractUser): 
    #offline should be at index zero
    connectivity_status = [('offline','offline'), ('online', 'online')]
    
    # receiver will be called before deletion of object
    username = models.CharField(max_length = 50)
    avatar = models.URLField(null = True, blank = True)
    email = models.EmailField(unique=True, null = False, blank = False)
    is_artist = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default=False)
    last_deactivation = models.DateTimeField(null = True, blank = True)
    status = models.CharField(choices = connectivity_status, default='offline') 
    # password in serializer
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username



class MailOTP(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    otp = models.PositiveIntegerField(null=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True)