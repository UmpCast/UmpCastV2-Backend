from django_filters import rest_framework as filters
from ..models import Game


class GameFilter(filters.FilterSet):
    date_time = filters.IsoDateTimeFromToRangeFilter()

    class Meta:
        model = Game
        fields = ['division', 'date_time']
