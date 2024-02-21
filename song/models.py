from django.db import models
from album.models import *
from cloudinary.models import CloudinaryField
from user.models import User

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length = 500)
    image = models.ImageField(upload_to = 'image', null = True, blank = True)

    
    # image = CloudinaryField('image')
    created_at = models.DateField(auto_now_add = True)
    # duration = models.TimeField()
    credits = models.CharField(max_length = 10000)
    album = models.ForeignKey(Album, on_delete = models.CASCADE)
    likes = models.PositiveIntegerField(default = 0)
    artist_id = models.ForeignKey(User, on_delete = models.CASCADE)
    
    
    
    def __str__(self):
        return self.title