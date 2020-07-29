from rest_framework import permissions
from ..models import League, Division, Role, Level


class IsLevelOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        level = Level.objects.get(pk=view.kwargs['pk'])
        return request.user.is_manager() and level.league in request.user.leagues.accepted()


class LevelListQueryRequired(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        league_pk = request.query_params.get('league', None)
        if league_pk is None:
            return False
        if League.objects.filter(pk=league_pk).exists():
            league = League.objects.get(pk=league_pk)
            return league in request.user.leagues.accepted()
        else:
            return False


class IsRoleOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        role = Role.objects.get(pk=view.kwargs['pk'])
        return request.user.is_manager() and role.division.league in request.user.leagues.accepted()


class IsDivisionOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        division = Division.objects.get(pk=view.kwargs['pk'])
        return request.user.is_manager() and division.league in request.user.leagues.accepted()


class IsUmpireOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        user_pk = request.query_params.get('user', None)
        if user_pk is None:
            return True
        return request.user.pk == int(user_pk)


class IsLeagueOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        league = League.objects.get(pk=view.kwargs['pk'])
        return request.user.is_manager() and league in request.user.leagues.accepted()
