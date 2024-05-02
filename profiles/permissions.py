from rest_framework import permissions


class IsEditorTeacherOrAdminPermission(permissions.DjangoModelPermissions,):
    
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
    # def has_permission(self, request, view):
    #     user = request.user
    #     if user.is_editor_teacher or user.is_staff:
    #         return True
    #     return False

class IsEditorTeacherPermission(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
    # def has_permission(self, request, view):
    #     user = request.user
    #     if user.is_authenticated and user.is_editor_teacher:
    #         return True
    #     return False
    
class isTeacherPermission(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
    }

    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_authenticated and request.user.is_teacher
        return False
    # def has_permission(self, request, view):
    #     user = request.user
    #     if user.is_teacher:
    #         return True
    #     return False
    
class IsStaffPermission(permissions.DjangoModelPermissions):
    pass

class IsAccountOwnerPermission(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj