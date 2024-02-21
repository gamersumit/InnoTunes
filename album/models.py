from django.db import models

# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length = 200)
    image = models.ImageField(upload_to=None)
    album_likes = models.PositiveIntegerField(default = 0)
    # artist_id = models.ForeignKey()
    
    def __str__(self):
        return self.name
    