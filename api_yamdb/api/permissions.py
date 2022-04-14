from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.user.is_staff
        return request.user.is_superuser or request.user.is_admin


class IsAdminModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
            or request.user.is_moderator
            or request.user.is_admin
        )
