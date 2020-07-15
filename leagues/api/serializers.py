from rest_framework import serializers
from ..models import League, Division, Role, ApplyLeagueCode


class ApplyLeagueCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplyLeagueCode
        fields = ('pk', 'league', 'expiration_date')
        read_only_fields = ('pk', 'league')

    def validate_league(self, league):
        if self.context['request'].method != 'POST':
            return league
        if League.objects.get(pk=league) in self.context['request'].user.leagues.all():
            return league
        else:
            raise ValidationError("Can only create code for a league you own")

class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ('pk', 'title', 'division')
        read_only_fields = ('pk', 'division')

    def validate_division(self, division):
        if self.context['request'].method != 'POST':
            return division
        if Division.objects.get(pk=division).league in self.context['request'].user.leagues.all():
            return division
        else:
            raise ValidationError("Can only create role for a league you own")


class DivisionSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(source='role_set', many=True, read_only=True)

    class Meta:
        model = Division
        fields = ('pk', 'title', 'league', 'ts_id', 'roles')
        read_only_fields = ('pk', 'league')

    def validate_league(self, league):
        if self.context['request'].method != 'POST':
            return league
        if League.objects.get(pk=league) in self.context['request'].user.leagues.all():
            return league
        else:
            raise ValidationError("Can only create divison for a league you own")


class LeaguePrivateSerializer(serializers.ModelSerializer):
    divisions = DivisionSerializer(source='division_set', many=True, read_only=True)

    class Meta:
        model = League
        fields = ('pk', 'title', 'description', 'divisions', 'league_picture', 'public_access',
                  'date_joined', 'expiration_date', 'adv_scheduling_limit', 'ts_id', 'opponent_library')
        read_only_fields = ('pk', 'date_joined')


class LeaguePublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = League
        fields = ('pk', 'title', 'description', 'league_picture')
        read_only_fields = ('pk',)