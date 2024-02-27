from django.db import models
from user.models import User
from music.models import Song

# Create your models here.

class Comment(models.Model):
    song_id = models.ForeignKey(Song, on_delete = models.CASCADE)   ## foreign key
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    description = models.CharField(max_length = 1000000)
    
    def __str__(self):
        return self.description
    