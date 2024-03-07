from utils.utils import CommonUtils
from django.dispatch import receiver
from django.db import models
from .models import Album, Song, Playlist, SongsInAlbum
import logging 
logger = logging.getLogger( __name__ )

# pre deltion playlist
@receiver(models.signals.pre_delete, sender=Playlist)
def delete_playlist(sender, instance, **kwargs):
  try:
    if instance.playlist_picture:
      # delete the avatar media from cloudinary
       CommonUtils.delete_media_from_cloudinary([instance.playlist_picture])

  except Exception as e:
    
    
    
# pre deltion album
@receiver(models.signals.pre_delete, sender=Album)

def delete_album(sender, instance, **kwargs):
    
    if instance.album_picture:
      # delete the album_picture media from cloudinary
       CommonUtils.delete_media_from_cloudinary([instance.album_picture])
  
    songs = SongsInAlbum.objects.filter(album_id = instance.id)
    songs.delete()
 
    
    
# pre deltion Song
@receiver(models.signals.pre_delete, sender=Song)
def delete_song(sender, instance, **kwargs):
    
    media = []
    if instance.song_picture:
      media.append(instance.song_picture)
    if instance.audio:
      media.append(instance.audio)
    if instance.song_picture:
      media.append(instance.audio)
    
    if media :
      # delete the avatar media from cloudinary
      CommonUtils.delete_media_from_cloudinary(media)
    