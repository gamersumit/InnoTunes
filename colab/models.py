from django.db import models
from music.models import Song
from user.models import User
# Create your models here.
class Colab(models.Model):
    song_id = models.ForeignKey(Song, on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    audio = models.URLField()
    video = models.URLField(null = True, blank = True)
    colab_picture = models.URLField(null=True, blank = True)
    audio_duration = models.CharField(max_length = 200, default = 0)
    created_at = models.DateField(auto_now_add = True)
    colab_name = models.CharField(max_length=255, default = 'colab')
    
    
    def __str__(self):
        return self.colab_name
