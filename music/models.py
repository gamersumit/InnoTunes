from cloudinary.models import CloudinaryField
from django.db import models
from user.models import User


# Album structure
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
    playlist_picture = models.URLField(blank=True, null=True)
    is_global = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user_id', 'playlist_name']
        
        
    def __str__(self):
        return self.playlist_name
    
class Genre(models.Model):
    genre = models.CharField(max_length = 20, primary_key=True)
    genre_picture = models.URLField(null = True, blank = True)

    def __str__(self):
        return self.genre
    
    
# Song structure
class Song(models.Model):
    # genre_choices = [
    #     ('Rock', 'Rock'),
    #     ('Jazz', 'Jazz'),
    #     ('EDM', 'EDM'),
    #     ('Pop', 'Pop'),
    #     ('Dubstep', 'Dubstep'),
    #     ('Disco', 'Disco'),
    #     ('Techno', 'Techno'),
    #     ('Hard Rock', 'Hard Rock'),
    #     ('Jungle Music', 'Jungle Music'),
    #     ('Classical', 'Classical'),
    #     ('Blues', 'Blues'),
    #     ('Other', 'Other')
    # ]
    
    artist_id = models.ForeignKey(User, on_delete = models.CASCADE)
    
    song_name = models.CharField(max_length = 500, unique=True)
    song_picture = models.URLField(null = True, blank = True)
    song_description = models.TextField(max_length = 100000, null = True, blank = True)
    
    audio = models.URLField()
    video = models.URLField(null = True, blank = True)
    audio_duration = models.PositiveIntegerField()
      
    genre = models.ForeignKey(Genre, default='Other', on_delete=models.SET_NULL, null=True, blank=True)    
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

    class Meta :
        unique_together = ['playlist_id', 'song_id']

# songs Inside Playlist
class RecentSongs(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    song_id = models.ForeignKey(Song, on_delete = models.CASCADE)
    last_played_at = models.DateTimeField(auto_now = True)
    

# Songs in Album Model   
class SongsInAlbum(models.Model):
    song_id = models.OneToOneField(Song, on_delete=models.CASCADE, unique=True)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    
    class Meta :
        unique_together = ['album_id', 'song_id']


class CurrentlyPlaying(models.Model):
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    user_id = models.OneToOneField(User, primary_key=True, on_delete = models.CASCADE)