from rest_framework import permissions
from utils.utils import UserUtils
from .models import Album, Playlist

# palylist owner permissons
class IsPlaylistOwnerOrReadOnly(permissions.DjangoModelPermissions):
    permission_queryset = None

    perms_map = {
       # 'GET': [],   // original
        'OPTIONS': [],
        'HEAD': [],
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        
        try :
            token = request.headers['Authorization'].split(' ')[1]
            token_user = UserUtils.getUserFromToken(token)
            id = request.data.get('playlist_id') 
            playlist = Playlist.objects.get(id = id)
            if not playlist :
              raise Exception('Playlist does\'nt exist')
            # Write permissions are only allowed to the owner of the playlist.
            return playlist.user_id == token_user
        
        except Exception as e:
            return False

#album owner permissions
class IsAlbumOwnerOrReadOnly(permissions.DjangoModelPermissions):
    permission_queryset = None

    perms_map = {
       # 'GET': [],   // original
        'OPTIONS': [],
        'HEAD': [],
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        
        try :
            token = request.headers['Authorization'].split(' ')[1]
            token_user = UserUtils.getUserFromToken(token)
            id = request.data.get('playlist_id')
            album = Album.objects.get(id = id)
            if not album :
              raise Exception('Playlist does\'nt exist')
            
            # Write permissions are only allowed to the owner of the playlist.
            return album.user_id == token_user
        
        except Exception as e:
            return False        