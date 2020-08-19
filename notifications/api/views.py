from ..models import (
    UmpCastNotification, LeagueNotification, GameNotification, ApplicationNotification
)
from backend.permissions import (
    IsSuperUser
)
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from django.db.models import Value, CharField, F
from rest_framework import serializers
from games.models import Application
from users.models import User


class NotificationObjectSerializer(serializers.Serializer):
    pk = serializers.CharField()
    subject = serializers.CharField()
    message = serializers.CharField()
    scope = serializers.CharField()
    notification_date_time = serializers.DateTimeField()
    related_pk = serializers.IntegerField()


class IsUserOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return User.objects.get(pk=view.kwargs.get('pk')) == request.user


class NotificationListView(ListAPIView):
    serializer_class = NotificationObjectSerializer
    permission_classes = (IsSuperUser | (permissions.IsAuthenticated & IsUserOwner), )
    value_fields = ('pk', 'subject', 'message', 'notification_date_time')

    def get_umpcast_qs(self):
        return UmpCastNotification.objects.all().values(
            *self.value_fields, scope = Value('ump-cast', output_field=CharField()), related_pk=F('pk')
        )

    def get_league_qs(self):
        pk = self.kwargs.get('pk')
        return LeagueNotification.objects.filter(league__user__pk=pk).values(
            *self.value_fields, scope = Value('league', output_field=CharField()), related_pk=F('league__pk')
        )

    def get_game_qs(self):
        pk = self.kwargs.get('pk')
        game_ids = Application.objects.filter(user__pk=pk).values_list('post__game__pk', flat=True)
        return GameNotification.objects.filter(game__pk__in=game_ids).values(
            *self.value_fields, scope = Value('game', output_field=CharField()), related_pk=F('game__pk')
        )

    def get_application_qs(self):
        pk = self.kwargs.get('pk')
        return ApplicationNotification.objects.filter(application__user__pk=pk).values(
            *self.value_fields, scope = Value('application', output_field=CharField()), related_pk=F('application__pk')
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