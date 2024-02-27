from cloudinary.models import CloudinaryField
from django.db import models
from user.models import User

class Album(models.Model):
    album_name = models.CharField(max_length = 200, unique=True)
    album_description = models.TextField(max_length = 50000)
    album_picture = models.URLField(null=True, blank=True)
    artist_id = models.ForeignKey(User, on_delete = models.CASCADE) ## if artist gets deleted, his album must not be deleted    
    
    def __str__(self):
        return self.album_name
    
# Playlist Structure : users can create playlist for themselves 
class Playlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=50)
    playlist_picture = models.URLField(blank = True)

    class Meta:
        unique_together = ['user_id', 'playlist_name']
        
        
    def __str__(self):
        return self.playlist_name

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
    
    song_name = models.CharField(max_length = 500)
    song_picture = models.URLField(null = True, blank = True)
    song_description = models.TextField(max_length = 100000, null = True, blank = True)
    
    audio = models.URLField(null = True, blank = True)
    video = models.URLField(null = True, blank = True)
    audio_duration = models.PositiveIntegerField(default = 0)
    
    genre = models.CharField(choices = genre_choices, null = False, blank=False)    
    lyrics = models.TextField(max_length = 100000, null=True, blank=True)
    credits = models.CharField(max_length = 10000, null = True, blank = True)
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
        
        
from re import T
from album.models import *
from cloudinary.models import CloudinaryField
from django.db import models
from user.models import User


# Album structure



# Song structure
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
    
    
    
    
    def __str__(self):
        return self.song_name

      
# <! -------------- Realtionship between Songs and Playlist/Album -------------------!>    


# songs Inside Playlist
class SongsInPlaylist(models.Model):
    playlist_id = models.ForeignKey(Playlist, on_delete = models.CASCADE)
    song_id = models.ForeignKey(Song, on_delete = models.CASCADE)

    class Meta :
        unique_together = ['playlist_id', 'song_id']

# Songs in Album Model   
class SongsInAlbum(models.Model):
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    
    class Meta :
        unique_together = ['album_id', 'song_id']