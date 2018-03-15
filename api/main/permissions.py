from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """
    Custom permission class to restrict access to only superusers.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission class to restrict access for
    object creation, update and deletion to only superusers.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_superuser


class DisallowCreateOrUpdate(BasePermission):
    """
    Custom permission class to not allow post http method.
    """

    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT']:
            return False
        return True
