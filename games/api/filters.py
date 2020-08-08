from django_filters import rest_framework as filters
from ..models import Game


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    """
    https://django-filter.readthedocs.io/en/latest/ref/filters.html#baseinfilter
    """


class GameFilter(filters.FilterSet):
    date_time = filters.IsoDateTimeFromToRangeFilter()
    division__in = NumberInFilter(field_name='division__pk', lookup_expr='in')

    class Meta:
        model = Game
        fields = ['division', 'date_time']
