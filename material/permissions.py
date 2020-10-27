from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsOwnAccount(permissions.BasePermission):
    """
    Allow a user to only view and edit their own account.
    """
    def has_object_permission(self, request, view, obj):
        # If we wanted to read other users' data:
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        return request.user and request.user == obj
