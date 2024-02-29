from django.db import models
from music.models import Song
from user.models import User
# Create your models here.
class Colab(models.Model):
    song_id = models.ForeignKey(Song, on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    colab_audio = models.FileField()
    colab_video = models.FileField()
    colab_pic = models.ImageField(upload_to = None)
    audio_duration = models.TimeField()
    date_added = models.DateField(auto_now_add = True)
    
    def __str__(self):
        self.song_id