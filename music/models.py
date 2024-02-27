from django.db import models
# from album.models import Album
from cloudinary.models import CloudinaryField
from django.db import models
from user.models import User


# Create your models here.
class Album(models.Model):
    album_name = models.CharField(max_length = 200)
    album_picture = models.ImageField(upload_to=None)
    album_description = models.TextField(max_length = 50000)
    total_likes = models.PositiveIntegerField(default = 0)
    
    # artist_id = models.ForeignKey(User, on_delete=models.CASCADE)
    artist_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) ## if artist gets deleted, his album must not be deleted    
    
    def __str__(self):
        return self.name
    
class Song(models.Model):
    artist_id = models.ForeignKey(User, on_delete = models.CASCADE)
    album_id = models.ForeignKey(Album, on_delete = models.CASCADE)
    
    title = models.CharField(max_length = 500)
    lyrics = models.CharField(max_length = 10000000, null=True, blank=True)
    credits = models.CharField(max_length = 10000)
    image = models.ImageField(upload_to = 'image/', null = True, blank = True)
    audio = models.FileField(upload_to='audio/', null=True, blank=True)
    video = models.FileField(upload_to='video/', null=True, blank=True)
    audio_duration = models.PositiveIntegerField()
    # image = CloudinaryField('image')
    # duration = models.TimeField()
    created_at = models.DateField(auto_now_add = True)
    
    def __str__(self):
        return self.title

    
# users can create playlist for themselves
class Playlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class SongsInPlaylist(models.Model):
    playlist_id = models.ForeignKey(Playlist, on_delete = models.CASCADE)
    song_id = models.ForeignKey(Song, on_delete = models.CASCADE)




class SongsInAlbum(models.Model):
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)    
