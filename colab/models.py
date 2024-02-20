from django.db import models
from song.models import Song
from user.models import User

# Create your models here.
class Colab(models.Model):
    song_id = models.ForeignKey(Song, on_delete = models.CASCADE)
    user_audio = models.FileField()
    user_video = models.FileField()
    colab_pic = models.ImageField(upload_to = None)
    duration = models.TimeField()
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        self.song_id