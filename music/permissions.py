from rest_framework import permissions
from utils.utils import UserUtils
from .models import *

class IsPlaylistOwner(permissions.BasePermissions):
    """
    Custom permission to only allow Playlist Owner to add or delete songs.
    """

    def has_object_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET
        try :
            token = self.request.headers['Authorization'].split(' ')[1]
            user = UserUtils.getUserFromToken(token).id
             
            if Playlist.objects.filters(user_id = user, id = request.data['playlist_id']).exist() :
              return True
            # Write permissions are only allowed to the owner of the playlist.
            
        
        except Exception as e:
            raise Exception(str(e)) 
    

class IsAlbumOwner(permissions.BasePermissions):
    """
    Custom permission to only allow album Owner to add or delete songs.
    """

    def has_object_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET
        try :
            token = self.request.headers['Authorization'].split(' ')[1]
            user = UserUtils.getUserFromToken(token).id
             
            if Album.objects.filters(user_id = user, id = request.data['album_id']).exist() :
              return True
            # Write permissions are only allowed to the owner of the playlist.
            
        
        except Exception as e:
            raise Exception(str(e)) 