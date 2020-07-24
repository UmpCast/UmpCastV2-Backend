from ..models import User, UserLeagueStatus
from rest_framework import permissions


class IsUserOwner(permissions.BasePermission):
    """
    Check if request user owns profile or is viewing personal profile
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if view.kwargs['pk'] == 'me':
            return True
        user = User.objects.get(pk=view.kwargs['pk'])
        return user == request.user


class IsLeagueMember(permissions.BasePermission):
    """
    Check if request user has valid user-list query scope
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        league_pk = request.query_params.get('league', None)
        if league_pk is not None and request.user.leagues.filter(pk=league_pk).exists():
            return True
        return request.user.is_superuser


class IsUserLeagueStatusOwner(permissions.BasePermission):
    """
    Check if request user is the owner of the UserLeagueStatus
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return UserLeagueStatus.objects.filter(pk=view.kwargs['pk'], user=request.user).exists()
