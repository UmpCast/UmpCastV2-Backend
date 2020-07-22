from rest_framework import serializers
from ..models import League, Division, Role
from rest_framework.serializers import ValidationError
from backend import mixins


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ('pk', 'title', 'division')
        read_only_fields = ('pk',)
        # create_only_fields = ('division',)

    def validate_division(self, division):
        if self.context['request'].method != 'POST':
            return division
        if division.league in self.context['request'].user.leagues.all():
            return division
        else:
            raise ValidationError("Can only create role for a league you own")


class DivisionSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(source='role_set', many=True, read_only=True)

    class Meta:
        model = Division
        fields = ('pk', 'title', 'league', 'ts_id', 'roles')
        read_only_fields = ('pk',)
        # create_only_fields = ('league', )

    def validate_league(self, league):
        if self.context['request'].method != 'POST':
            return league
        if league in self.context['request'].user.leagues.all():
            return league
        else:
            raise ValidationError("Can only create divison for a league you own")


class LeaguePrivateSerializer(serializers.ModelSerializer):
    divisions = DivisionSerializer(source='division_set', many=True, read_only=True)

    class Meta:
        model = League
        fields = ('pk', 'title', 'description', 'divisions', 'league_picture', 'public_access',
                  'date_joined', 'expiration_date', 'adv_scheduling_limit', 'ts_id', 'opponent_library', 'can_apply')
        read_only_fields = ('pk', 'date_joined')


class LeaguePublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = League
        fields = ('pk', 'title', 'description', 'league_picture', 'can_apply')
        read_only_fields = ('pk', 'title', 'description', 'league_picture', 'can_apply')
