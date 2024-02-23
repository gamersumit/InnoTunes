from rest_framework import permissions

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