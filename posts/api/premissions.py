from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Allows access only to author or admin or readonly.
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_staff
        )


class IsAuthenticatedOrAdmin(permissions.BasePermission):
    """
    Allows access only admin to safe methods and
    allows access authenticated user and admin to unsafe method.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user.is_staff)
        elif request.method not in permissions.SAFE_METHODS:
            return bool(
                request.user and request.user.is_authenticated or request.user.is_staff
            )
