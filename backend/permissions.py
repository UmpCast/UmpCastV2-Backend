from rest_framework import permissions


class ActionBasedPermission(permissions.AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """
    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser


class IsManager(permissions.BasePermission):
    """
    Check to see if a user is a manager
    """
    def has_permission(self, request, view):
        return request.user.is_manager()
