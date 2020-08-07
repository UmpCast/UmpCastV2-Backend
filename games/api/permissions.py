from ..models import Application, Post, Game
from rest_framework import permissions
from leagues.models import Division, League

class IsApplicationLeague(permissions.BasePermission):
    """
    Checks to see if a manager is owner of an application
    """
    def has_permission(self, request, view):
        return Application.objects.get(pk=view.kwargs['pk']).post.game.division.league in request.user.leagues.accepted()


class IsPostLeague(permissions.BasePermission):
    """
    Checks to see if a manager is owner of a post
    """
    def has_permission(self, request, view):
        return Post.objects.get(pk=view.kwargs['pk']).game.division.league in request.user.leagues.accepted()


class IsGameLeague(permissions.BasePermission):
    """
    Checks to see if a manager is owner of a game
    """
    def has_permission(self, request, view):
        return Game.objects.get(pk=view.kwargs['pk']).division.league in request.user.leagues.accepted()


class GameFilterPermissions(permissions.BasePermission):
    """
    FilterPermissions for Game List View.
    Can only filter league/division if accepted to respective league, cannot list all games
    """
    def has_permission(self, request, view):
        division_pk = request.query_params.get('division', None)
        if division_pk is None:
            return False
        return Division.objects.get(pk=division_pk).league in request.user.leagues.accepted()


class ListByDivisionPermission(permissions.BasePermission):
    """
    ListByDivision Permission Rules
    Can only filter by divisions in which the user is in the league for
    """
    def has_permission(self, request, view):
        division_list = request.data.get('divisions', None)
        for division in division_list:
            if Division.objects.get(pk=division).league not in request.user.leagues.accepted():
                return False
        return True
