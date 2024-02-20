from django.db import models
from album.models import *

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length = 500)
    image = models.ImageField(upload_to = None, null = True, blank = True)
    date_added = models.DateTimeField()
    duration = models.TimeField()
    credits = models.CharField(max_length = 10000)
    album = models.ForeignKey(Album, on_delete = models.CASCADE)
    likes = models.PositiveIntegerField(default = 0)
    # artist_id = models.ForeignKey(Artist)
   
    
    def __str__(self):
        return self.title