from album.models import *
from cloudinary.models import CloudinaryField
from django.db import models
from user.models import User


# Create your models here.
class Song(models.Model):
    genre_choices = [
        ('Rock', 'Rock'),
        ('Jazz', 'Jazz'),
        ('EDM', 'EDM'),
        ('Pop', 'Pop'),
        ('Dubstep', 'Dubstep'),
        ('Disco', 'Disco'),
        ('Techno', 'Techno'),
        ('Hard Rock', 'Hard Rock'),
        ('Jungle Music', 'Jungle Music'),
        ('Classical', 'Classical'),
        ('Blues', 'Blues'),
        ('Other', 'Other')
    ]
    
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
        return self.song_name

      
# <! -------------- Realtionship between Songs and Playlist/Album -------------------!>    


# songs Inside Playlist
class SongsInPlaylist(models.Model):
    playlist_id = models.ForeignKey(Playlist, on_delete = models.CASCADE)
    song_id = models.ForeignKey(Song, on_delete = models.CASCADE)




class SongsInAlbum(models.Model):
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)    

    class Meta :
        unique_together = ['playlist_id', 'song_id']

# Songs in Album Model   
class SongsInAlbum(models.Model):
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    
    class Meta :
        unique_together = ['album_id', 'song_id']