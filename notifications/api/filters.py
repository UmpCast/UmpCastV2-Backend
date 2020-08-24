from django_filters import rest_framework as filters
from ..models import UmpCastNotification, LeagueNotification, GameNotification, ApplicationNotification
from games.models import Application


class UmpCastNotificationFilter(filters.FilterSet):
    date_time = filters.IsoDateTimeFromToRangeFilter(
        field_name='notification_date_time')

    class Meta:
        model = UmpCastNotification
        fields = ['date_time']


class LeagueNotificationFilter(filters.FilterSet):
    date_time = filters.IsoDateTimeFromToRangeFilter(
        field_name='notification_date_time')
    user = filters.CharFilter(field_name='league__user', lookup_expr='pk')

    class Meta:
        model = LeagueNotification
        fields = ['date_time', 'league']


class GameNotificationFilter(filters.FilterSet):
    date_time = filters.IsoDateTimeFromToRangeFilter(
        field_name='notification_date_time')
    user = filters.CharFilter(method='game_filter_by_user')

    class Meta:
        model = GameNotification
        fields = ['date_time']

    def game_filter_by_user(self, queryset, name, value):
        game_ids = Application.objects.filter(
            user__pk=value).values_list('post__game__pk', flat=True)
        return queryset.filter(game__pk__in=game_ids)


class ApplicationNotificationFilter(filters.FilterSet):
    date_time = filters.IsoDateTimeFromToRangeFilter(
        field_name='notification_date_time')
    user = filters.CharFilter(field_name='application__user', lookup_expr='pk')

    class Meta:
        model = ApplicationNotification
        fields = ['date_time']
