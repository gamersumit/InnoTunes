from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class ListenerUser(AbstractUser):
    name = models.CharField(max_length = 50)
    image = models.ImageField(upload_to = None, null = True, blank = True)
    email = models.EmailField()
    isArtist = models.BooleanField(default = False)
    # password in serializer
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name
    


from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class AdminUser(AbstractUser):
    name = models.CharField(max_length = 50)
    image = models.ImageField(upload_to = None, null = True, blank = True)
    email = models.EmailField()
    isVerified = models.BooleanField(default=False)
    # password in serialize
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name