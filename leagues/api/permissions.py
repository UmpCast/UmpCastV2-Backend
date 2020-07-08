from rest_framework import permissions
from ..models import League, Division, Role, ApplyLeagueCode


class IsCodeOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        code = ApplyLeagueCode.objects.get(pk=view.kwargs['pk'])
        return request.user.is_manager() and code.league in request.user.leagues.all()


class ListCodePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        league_pk = self.request.query_params.get('league', None)
        if league_pk is None:
            return request.user.is_superuser
        return request.user.is_manager() and League.objects.get(pk=league_pk) in request.user.leagues.all()

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_manager()


class IsRoleOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        role = Role.objects.get(pk=view.kwargs['pk'])
        return request.user.is_manager() and role.division.league in request.user.leagues.all()


class IsDivisionOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        division = League.objects.get(pk=view.kwargs['pk'])
        return request.user.is_manager() and division.league in request.user.leagues.all()


class IsUmpireOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        user_pk = self.request.query_params.get('user', None)
        if user_pk is None:
            return True
        return request.user.pk == user_pk


class IsLeagueOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        league = League.objects.get(pk=view.kwargs['pk'])
        return request.user.is_manager() and league in request.user.leagues.all()
