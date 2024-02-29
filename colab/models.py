from django.db import models
from music.models import Song
from user.models import User
# Create your models here.
class Colab(models.Model):
    song_id = models.ForeignKey(Song, on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    colab_audio = models.URLField(null = True, blank = True)
    colab_video = models.URLField(null = True, blank = True)
    colab_picture = models.URLField(null = True, blank = True)
    audio_duration = models.CharField(max_length = 200, default = 0)
    date_added = models.DateField(auto_now_add = True)
    
    def __str__(self):
        self.song_id