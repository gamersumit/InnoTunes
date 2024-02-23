# from django.db import models
# from user.models import User
# from music.models import Song

# Create your models here.
# class Album(models.Model):
#     album_name = models.CharField(max_length = 200)
#     album_picture = models.ImageField(upload_to=None)
#     album_description = models.TextField(max_length = 50000)
#     total_likes = models.PositiveIntegerField(default = 0)
    
#     # artist_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     artist_id = models.ForeignKey(User) ## if artist gets deleted, his album must not be deleted    
    
#     def __str__(self):
#         return self.name

# class SongsInAlbum(models.Model):
#     song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
#     album_id = models.ForeignKey(Album, on_delete=models.CASCADE)    
    
    