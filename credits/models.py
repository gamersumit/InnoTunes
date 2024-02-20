from django.db import models


class Credits(models.Model):
    artist_name = models.CharField(max_length = 200)
    composer = models.CharField(max_length = 200)
    lyricist = models.CharField(max_length = 200)
    song_id = models.IntegerField(default = None)   ## fore
