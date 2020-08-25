from rest_framework import permissions
from ..models import League, Division, Role, Level
from users.models import User


class InLevelLeague(permissions.BasePermission):
    """
    Checks to see if a user has access rights to a level in a given league
    """

    def has_permission(self, request, view):
        level = Level.objects.get(pk=view.kwargs['pk'])
        return level.league in request.user.leagues.accepted()


class LevelListQueryRequired(permissions.BasePermission):
    """
    Checks to see if a user has viewing rights to a filtered list of levels
    """

    def has_permission(self, request, view):
        league_pk = request.query_params.get('league', None)
        if league_pk is None:
            return False
        if League.objects.filter(pk=league_pk).exists():
            league = League.objects.get(pk=league_pk)
            return league in request.user.leagues.accepted()
        else:
            return False


class InRoleLeague(permissions.BasePermission):
    """
    Checks to see if a user has access rights to a given role
    """

    def has_permission(self, request, view):
        role = Role.objects.get(pk=view.kwargs['pk'])
        return role.division.league in request.user.leagues.accepted()


class InDivisionLeague(permissions.BasePermission):
    """
    Checks to see if a user has access rights to a given division
    """

    def has_permission(self, request, view):
        division = Division.objects.get(pk=view.kwargs['pk'])
        return division.league in request.user.leagues.accepted()


class IsUmpireOwner(permissions.BasePermission):
    """
    List all leagues if no user_pk is supplied. If supplied, must be current user
    """

    def has_permission(self, request, view):
        user_pk = request.query_params.get('user', None)
        if user_pk is None:
            return False
        return request.user == User.objects.get(pk=user_pk)


class InLeague(permissions.BasePermission):
    """
    Checks to see if a given user has access rights to a given league
    """

    def has_permission(self, request, view):
        league = League.objects.get(pk=view.kwargs['pk'])
        return league in request.user.leagues.accepted()
