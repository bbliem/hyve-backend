from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
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


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    Assumes the model instance has a `user` attribute indicating the owner.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsMemberOfThisOrganization(permissions.BasePermission):
    """
    Object-level permission to only allow members of an organization to access the organization.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.organization == obj
