from django.db import models
from user.models import User
from music.models import Song, Album, Playlist

# Create your models here.

class Comment(models.Model):
    song_id = models.ForeignKey(Song, on_delete = models.CASCADE)   ## foreign key
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    description = models.CharField(max_length = 1000000)
    
    def __str__(self):
        return self.description


# Follower pattern
class Followers(models.Model) :
    artist_id = models.ForeignKey(User, related_name = 'following', on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, related_name = 'follower', on_delete = models.CASCADE)
    
    class Meta:
        unique_together = ['artist_id', 'user_id']
    
    @staticmethod    
    def get_total_followers(artist):
        return Followers.objects.filter(artist_id = artist).count()  
    
    @staticmethod
    def get_total_following(artist):
        return Followers.objects.filter(user_id = artist).count() 
    

# Liked Album Model
class AlbumLikes(models.Model) :
    album_id = models.ForeignKey(Album,  on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    
    class Meta:
        unique_together = ['album_id', 'user_id']
    
    @staticmethod    
    def get_total_likes(self, album):
        return AlbumLikes.objects.filter(album_id = album).count()
    
    
# Liked Playlist Model
class PlaylistLikes(models.Model) :
    playlist_id = models.ForeignKey(Playlist,  on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    
    class Meta:
        unique_together = ['playlist_id', 'user_id']
    
    @staticmethod    
    def get_total_likes(self, playlist):
        return PlaylistLikes.objects.filter(playlist_id = playlist).count()
    

# Liked Songs Model
class SongLikes(models.Model) :
    song_id = models.ForeignKey(Song,  on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    
    class Meta:
        unique_together = ['song_id', 'user_id']
    
    @staticmethod    
    def get_total_likes(self, song):
        return SongLikes.objects.filter(song_id = song).count()