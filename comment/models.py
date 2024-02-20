from django.db import models

# Create your models here.

class Comment(models.Model):
    song_id = models.IntegerField(default = None)   ## foreign key
    user_id = models.IntegerField(default = None)   ## foreign key
    description = models.CharField(max_length = 1000000)