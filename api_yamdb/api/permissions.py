from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == request.user.ADMIN or request.user.is_staff:
            return True
        return False
