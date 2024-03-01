from rest_framework import permissions

from utils.utils import UserUtils

# class for normal user / Audiance
class IsUserOwnerOrReadOnly(permissions.DjangoModelPermissions):
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
            request_user = request.data.get('user_id')
            # Write permissions are only allowed to the owner of the playlist.
            return request_user == str(token_user.id)
        
        except Exception as e:
            return False
        
class IsArtistOwnerOrReadOnly(permissions.DjangoModelPermissions):
    """
    Custom permission to only allow Artist to perform actions.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET
        if request.method == 'GET':
            return True
        
        try :
            token = request.headers['Authorization'].split(' ')[1]
            token_user = UserUtils.getUserFromToken(token)
            request_user = request.data.get('artist_id')
    
            return token_user.is_artist and request_user == str(token_user.id)
        
        except Exception as e:
            return False
