from ..models import (
    UmpCastNotification, LeagueNotification, GameNotification, ApplicationNotification, BaseNotification
)

from rest_framework import serializers
from rest_framework.serializers import ValidationError


class UmpCastNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UmpCastNotification
        fields = ('pk', 'notification_date_time', 'subject', 'message')
        read_only_fields = ('pk', 'notification_date_time')


class LeagueNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeagueNotification
        fields = ('pk', 'notification_date_time',
                  'subject', 'message', 'league')
        read_only_fields = ('pk', 'notification_date_time')

    def validate_league(self, league):
        if league in self.context['request'].user.leagues.accepted():
            return league
        else:
            raise ValidationError(
                "Can only create LeagueNotification for a league you own")


class GameNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameNotification
        fields = ('pk', 'notification_date_time', 'subject', 'message', 'game')
        read_only_fields = ('pk', 'notification_date_time')


class ApplicationNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationNotification
        fields = ('pk', 'notification_date_time',
                  'subject', 'message', 'application')
        read_only_fields = ('pk', 'notification_date_time')
