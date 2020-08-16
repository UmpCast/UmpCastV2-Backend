from rest_framework import permissions
from leagues.models import League


class TeamSnapNoteFilterPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        league = request.query_params.get('league', None)
        if league is None:
            return False
        return League.objects.get(pk=league) in request.user.leagues.accepted()


class InLeague(permissions.BasePermission):
    def has_permission(self, request, view):
        return League.objects.get(pk=view.kwargs['pk']) in request.user.leagues.accepted()
