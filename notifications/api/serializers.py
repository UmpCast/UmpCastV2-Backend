from ..models import (
    UmpCastNotification, LeagueNotification, GameNotification, ApplicationNotification, BaseNotification
)

from rest_framework import serializers


class UmpCastNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UmpCastNotification
        fields = ('pk', 'notification_date_time', 'subject', 'message')
        read_only_fields = ('pk', 'notification_date_time')


class LeagueNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeagueNotification
        fields = ('pk', 'notification_date_time', 'subject', 'message', 'league')
        read_only_fields = ('pk', 'notification_date_time')


class GameNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameNotification
        fields = ('pk', 'notification_date_time', 'subject', 'message', 'game')
        read_only_fields = ('pk', 'notification_date_time')


class ApplicationNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationNotification
        fields = ('pk', 'notification_date_time', 'subject', 'message', 'application')
        read_only_fields = ('pk', 'notification_date_time')
