from rest_framework import permissions


class IsOwnAccountOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow a user to only edit their own account.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user