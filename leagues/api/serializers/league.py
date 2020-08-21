from rest_framework import serializers

from leagues.models import League
from users.models import UserLeagueStatus

from .division import DivisionRetrieveSerializer
from .level import LevelRetrieveSerializer


class LeaguePrivateSerializer(serializers.ModelSerializer):
    divisions = DivisionRetrieveSerializer(
        source='division_set', many=True, read_only=True)
    levels = LevelRetrieveSerializer(
        source='level_set', many=True, read_only=True)

    class Meta:
        model = League
        fields = ('pk', 'title', 'description', 'divisions', 'levels', 'league_picture', 'public_access',
                  'date_joined', 'expiration_date', 'adv_scheduling_limit',
                  'can_apply', 'website_url', 'email', 'default_max_casts', 'default_max_backups', 'cancellation_period', 'api_key', 'is_synced')
        read_only_fields = ('pk', 'date_joined')

    def create(self, validated_data):
        assert self.context['request'].user.is_manager(), (
            'this line should not be reachable. request user must be manager to create league'
        )
        league = super().create(validated_data)
        user = self.context['request'].user

        # adds user to league with request_status=accepted
        UserLeagueStatus.objects.create(
            user=user,
            league=league,
            request_status='accepted'
        )
        return league


class LeaguePublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = League
        fields = ('pk', 'title', 'description', 'league_picture',
                  'can_apply', 'website_url', 'email')
        read_only_fields = ('pk', 'title', 'description',
                            'league_picture', 'can_apply', 'website_url', 'email')
