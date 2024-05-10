from rest_framework import permissions

class IsAccountOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user == obj.owner.user) or (request.user.is_superuser)
        return False