from django_filters import rest_framework as filters
from ..models import UserLeagueStatus


class UserLeagueStatusFilter(filters.FilterSet):
    account_type = filters.CharFilter(field_name='user', lookup_expr='account_type')

    class Meta:
        model = UserLeagueStatus
        fields = ['user', 'league', 'request_status', 'account_type']
