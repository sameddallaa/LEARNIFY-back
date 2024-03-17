from rest_framework import permissions

class IsEditorTeacherPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        user = request.user
        if user.is_staff or user.is_editor_teacher:
            return True
        return False
    
class isTeacherPermission(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
    }
    
class IsStaffPermission(permissions.DjangoModelPermissions):
    pass