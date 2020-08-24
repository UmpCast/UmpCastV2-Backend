from django.db.models import CharField, F, Value
from rest_framework import permissions, serializers
from rest_framework.generics import ListAPIView

from backend.permissions import IsSuperUser
from games.api.serializers.application import ApplicationPublicSerializer
from games.api.serializers.game import GameSerializer
from games.models import Application, Game
from leagues.api.serializers.league import LeaguePublicSerializer
from leagues.models import League
from users.models import User

from ..models import (ApplicationNotification, GameNotification,
                      LeagueNotification, UmpCastNotification)


class NotificationObjectSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    subject = serializers.CharField()
    message = serializers.CharField()
    scope = serializers.CharField()
    notification_date_time = serializers.DateTimeField()
    related_pk = serializers.IntegerField()
    related_object = serializers.SerializerMethodField()

    def get_related_object(self, obj):
        scope = obj.get('scope')
        related_pk = obj.get('related_pk')
        if scope == 'ump-cast':
            return {}
        if scope == 'league':
            return LeaguePublicSerializer(League.objects.get(pk=related_pk)).data
        if scope == 'game':
            return GameSerializer(Game.objects.get(pk=related_pk)).data
        if scope == 'application':
            return ApplicationPublicSerializer(Application.objects.get(pk=related_pk)).data
        return {}


class IsUserOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return User.objects.get(pk=view.kwargs.get('pk')) == request.user


class NotificationListView(ListAPIView):
    serializer_class = NotificationObjectSerializer
    permission_classes = (IsSuperUser | (
        permissions.IsAuthenticated & IsUserOwner), )
    value_fields = ('pk', 'subject', 'message', 'notification_date_time')

    def get_umpcast_qs(self):
        return UmpCastNotification.objects.all().values(
            *self.value_fields, scope=Value('ump-cast', output_field=CharField()), related_pk=F('pk')
        )

    def get_league_qs(self):
        pk = self.kwargs.get('pk')
        return LeagueNotification.objects.filter(league__user__pk=pk).values(
            *self.value_fields, scope=Value('league', output_field=CharField()), related_pk=F('league__pk')
        )

    def get_game_qs(self):
        pk = self.kwargs.get('pk')
        game_ids = Application.objects.filter(
            user__pk=pk).values_list('post__game__pk', flat=True)
        return GameNotification.objects.filter(game__pk__in=game_ids).values(
            *self.value_fields, scope=Value('game', output_field=CharField()), related_pk=F('game__pk')
        )

    def get_application_qs(self):
        pk = self.kwargs.get('pk')
        return ApplicationNotification.objects.filter(application__user__pk=pk).values(
            *self.value_fields, scope=Value('application', output_field=CharField()), related_pk=F('application__pk')
        )

    def get_queryset(self):
        qs = self.get_umpcast_qs().union(
            self.get_league_qs()
        ).union(
            self.get_game_qs()
        ).union(
            self.get_application_qs()
        ).order_by('-notification_date_time')
        return qs
