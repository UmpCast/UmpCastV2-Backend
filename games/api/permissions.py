from ..models import Application, Post, Game
from rest_framework import permissions
from leagues.models import Division, League
from users.models import User

class IsApplicationLeague(permissions.BasePermission):
    """
    Checks to see if a manager is owner of an application
    """
    def has_permission(self, request, view):
        return Application.objects.get(pk=view.kwargs['pk']).post.game.division.league in request.user.leagues.accepted()


class ApplicationFilterPermission(permissions.BasePermission):
    """
    Applications must be filtered using user_pk. The user_pk must belong to the request user
    """
    def has_permission(self, request, view):
        user_pk = request.query_params.get('user', None)
        if user_pk is None:
            return False
        return User.objects.get(pk=user_pk) == request.user


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
        division__in = request.query_params.get('division__in', None)

        if division_pk is None and division__in is None:
            return False
        if division_pk is not None and Division.objects.get(pk=division_pk).league not in request.user.leagues.accepted():
            return False
        if division__in is not None:
            for division in division__in.split(','):
                if Division.objects.get(pk=division).league not in request.user.leagues.accepted():
                    return False
        return True
