from rest_framework import serializers
from ..models import League, Division, Role, Level
from rest_framework.serializers import ValidationError
from users.models import UserLeagueStatus


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ('pk', 'title', 'division')
        read_only_fields = ('pk',)
        # create_only_fields = ('division',)

    def validate_division(self, division):
        if self.context['request'].method != 'POST':
            return division
        if division.league in self.context['request'].user.leagues.accepted():
            return division
        else:
            raise ValidationError("Can only create role for a league you own")


class LevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Level
        fields = ('pk', 'title', 'league', 'visibilities', 'order')
        read_only_fields = ('pk', )
        create_only_fields = ('league', )

    def validate_league(self, league):
        if self.context['request'].method != 'POST':
            return league
        if league in self.context['request'].user.leagues.accepted():
            return league
        else:
            raise ValidationError("League can only be specified on creation/must be with a owned league")

    def update(self, instance, validated_data):  # remove create_only_fields from dictionary
        for field in LevelSerializer.Meta.create_only_fields:
            validated_data.pop(field, None)
        if 'visibilities' in validated_data:
            for visibility in validated_data['visibilities']:
                if visibility.division.league != instance.league:
                    raise ValidationError('roles in visibilities from wrong league added to level')
        return super().update(instance, validated_data)

    def validate(self, data):
        if self.context['request'].method == 'POST':
            for visibility in data['visibilities']:
                if visibility.division.league != data['league']:
                    raise ValidationError('roles in visibilities for level must be from league')
        return super().validate(data)


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
        if league in self.context['request'].user.leagues.accepted():
            return league
        else:
            raise ValidationError("Can only create divison for a league you own")


class LeaguePrivateSerializer(serializers.ModelSerializer):
    divisions = DivisionSerializer(source='division_set', many=True, read_only=True)
    levels = LevelSerializer(source='level_set', many=True, read_only=True)

    class Meta:
        model = League
        fields = ('pk', 'title', 'description', 'divisions', 'levels', 'league_picture', 'public_access',
                  'date_joined', 'expiration_date', 'adv_scheduling_limit', 'ts_id', 'opponent_library',
                  'can_apply', 'website_url', 'email', 'default_max_cast', 'default_max_backup')
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
        fields = ('pk', 'title', 'description', 'league_picture', 'can_apply', 'website_url', 'email')
        read_only_fields = ('pk', 'title', 'description', 'league_picture', 'can_apply', 'website_url', 'email')
