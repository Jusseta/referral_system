from rest_framework.permissions import BasePermission


class IsUser(BasePermission):
    """Checking if user is active"""
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        else:
            if request.user.is_active:
                return True
        return False


class IsSuperUser(BasePermission):
    """Checking if user is a superuser"""
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False
