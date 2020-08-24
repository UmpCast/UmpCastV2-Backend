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

# class IsUserFilter(permissions.BasePermission):
    # def has_permission(self, request, view):


class IsGameLeague(permissions.BasePermission):
    """
    Checks to see if a manager is owner of a game
    """

    def has_permission(self, request, view):
        return Game.objects.get(pk=view.kwargs['pk']).division.league in request.user.leagues.accepted()


class GameFilterDivision(permissions.BasePermission):
    def has_permission(self, request, view):
        division_pk = request.query_params.get('division', None)
        division_visibilities = request.user.leagues.values_list(
            'userleaguestatus__visibilities__division', flat=True)
        if division_pk:
            return int(division_pk) in division_visibilities
        return False


class GameFilterDivisionManager(permissions.BasePermission):
    def has_permission(self, request, view):
        division_pk = request.query_params.get('division', None)
        if division_pk:
            return Division.objects.get(pk=division_pk).league in request.user.leagues.accepted()
        return False


class GameFilterDivisionIn(permissions.BasePermission):
    def has_permission(self, request, view):
        division__in = request.query_params.get('division__in', None)
        division_visibilities = request.user.leagues.values_list(
            'userleaguestatus__visibilities__division', flat=True)
        if division__in:
            for division in division__in.split(','):
                if int(division) not in division_visibilities:
                    return False
            return True
        return False


class GameFilterDivisionInManager(permissions.BasePermission):
    def has_permission(self, request, view):
        division__in = request.query_params.get('division__in', None)
        if division__in:
            for division in division__in.split(','):
                if Division.objects.get(pk=int(division)).league not in request.user.leagues.accepted():
                    return False
            return True
        return False


class GameFilterUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.query_params.get('user', None)
        if user:
            return User.objects.get(pk=user) == request.user
        return False
