from rest_framework import permissions
from ..models import LeagueNotification, GameNotification
from users.models import User


class InLeague(permissions.BasePermission):
    """
    Checks to see if a given user has access rights to a given league
    """
    def has_permission(self, request, view):
        league_notification = LeagueNotification.objects.get(pk=view.kwargs['pk'])
        return league_notification.league in request.user.leagues.accepted()


class FilterUserOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        user_pk = request.query_params.get('user', None)
        if user_pk is None:
            return False
        return User.objects.get(pk=user_pk) == request.user


class InGameLeague(permissions.BasePermission):
    def has_permission(self, request, view):
        game_notification = GameNotification.objects.get(pk=view.kwargs['pk'])
        return game_notification.game.division.league in request.user.leagues.accepted()


class IsApplicationNotificationOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        application_notification = ApplicationNotification.objects.get(pk=view.kwargs['pk'])
        return application_notification.application.user.pk == request.user.pk
