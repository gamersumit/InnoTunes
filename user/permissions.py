from rest_framework import permissions

from utils.utils import UserUtils

# class for normal user / Audiance
class UserPermissions(permissions.DjangoModelPermissions):
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
        if not request.user.is_artist :
            return  True
        
        return False
    


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET
        if request.method == 'GET':
            return True
        
        try :
            token = self.request.headers['Authorization'].split(' ')[1]
            token_user = UserUtils.getUserFromToken(token).id
            request_user = request.data.get('owner_id')
            # Write permissions are only allowed to the owner of the playlist.
            return request_user == token_user 
        
        except Exception as e:
            raise Exception(str(e)) 
        
class IsArtistOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow Artist to perform actions.
    """

    def has_object_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET
        try :
            token = self.request.headers['Authorization'].split(' ')[1]
            user = UserUtils.getUserFromToken(token).id
            # Write permissions are only allowed to the owner of the playlist.
            return user.is_artist
        
        except Exception as e:
            raise Exception(str(e)) 

