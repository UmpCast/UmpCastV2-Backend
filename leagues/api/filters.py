from django_filters import rest_framework as filters

from leagues.models import League
from django.contrib.postgres.search import TrigramSimilarity


class LeagueFilter(filters.FilterSet):
    title = filters.CharFilter(method='title_trigram_search')

    class Meta:
        model = League
        fields = ['user']

    def title_trigram_search(self, queryset, name, value):
        return queryset.annotate(
            similarity=TrigramSimilarity('title', value)
        ).filter(similarity__gt=0.15)
