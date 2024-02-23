from album.models import *
from cloudinary.models import CloudinaryField
from django.db import models
from user.models import User

# <! ---------------- SONGS MODELS ----------------!>
# Create your models here.
class Song(models.Model):
    artist_id = models.ForeignKey(User, on_delete = models.CASCADE)
    album_id = models.ForeignKey(Album, on_delete = models.CASCADE)
    
    title = models.CharField(max_length = 500)
    lyrics = models.CharField(max_length = 10000000, null=True, blank=True)
    credits = models.CharField(max_length = 10000)
    image = models.ImageField(upload_to = 'image', null = True, blank = True)
     
    # image = CloudinaryField('image')
    # duration = models.TimeField()
    created_at = models.DateField(auto_now_add = True)
    
    
    def __str__(self):
        return self.title

      
# <! -------------- Playlist Models -------------------!>    
# users can create playlist for themselves
class Playlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    playlist_picture = models.ImageField(upload_to=None)

    def __str__(self):
        return self.title

# songs Inside Playlist
class SongsInPlaylist(models.Model):
    playlist_id = models.ForeignKey(Playlist, on_delete = models.CASCADE)
    song_id = models.ForeignKey(Song, on_delete = models.CASCADE)

# album inside Playlist    
class AlbumInPlaylist(models.Model):
    playlist_id = models.ForeignKey(Playlist, on_delete = models.CASCADE)
    album_id = models.ForeignKey(Album, on_delete = models.CASCADE)


# <! --------------Album Models -------------------!> 

# Album Model
class Album(models.Model):
    album_name = models.CharField(max_length = 200, unique=True)
    album_picture = models.ImageField(upload_to=None)
    album_description = models.TextField(max_length = 50000)
    artist_id = models.ForeignKey(User, on_delete = models.CASCADE) ## if artist gets deleted, his album must not be deleted    
    
    def __str__(self):
        return self.name
    
       
# Songs in Album Model   
class SongsInAlbum(models.Model):
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)