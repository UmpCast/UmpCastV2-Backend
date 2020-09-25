from django_filters import rest_framework as filters

from games.models import Application

from ..models import Application, Game


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    """
    https://django-filter.readthedocs.io/en/latest/ref/filters.html#baseinfilter
    """


class GameFilter(filters.FilterSet):
    date_time = filters.IsoDateTimeFromToRangeFilter()
    division__in = NumberInFilter(field_name='division__pk', lookup_expr='in')
    user = filters.CharFilter(method='game_filter_by_user')

    class Meta:
        model = Game
        fields = ['division', 'date_time']

    def game_filter_by_user(self, queryset, name, value):
        game_ids = Application.objects.filter(
            user__pk=value).values_list('post__game__pk', flat=True)
        return queryset.filter(pk__in=game_ids)


class ApplicationFilter(filters.FilterSet):
    date_time = filters.IsoDateTimeFromToRangeFilter(
        field_name='post__game__date_time')
    casted = filters.BooleanFilter(method='get_casted')

    class Meta:
        model = Application
        fields = ['user', 'date_time']

    def get_casted(self, queryset, name, value):
        app_ids = []
        for app in Application.objects.all().iterator():
            if app.is_casted() == value:
                app_ids.append(app.id)
        return Application.objects.filter(id__in=app_ids)
