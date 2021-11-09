from rest_framework import permissions


class IsAuthenticatedForDetailOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if (view.kwargs.get('pk') is not None
                and not request.user.is_authenticated):
            return False
        return True
