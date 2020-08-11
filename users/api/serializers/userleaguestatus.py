from users.models import UserLeagueStatus
from rest_framework.serializers import ValidationError
from leagues.api.serializers.league import LeaguePublicSerializer
from users.api.serializers.user import UserProfilePublicSerializer
from rest_framework import serializers

class UserLeagueStatusBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLeagueStatus
        fields = ('pk', 'user', 'league', 'date_pending', 'date_joined',
                    'request_status', 'max_casts', 'max_backups', 'visibilities')
        read_only_fields = ('pk', 'date_pending')


class UserLeagueStatusCreateSerializer(UserLeagueStatusBaseSerializer):

    def validate_user(self, user):
        if user != self.context['request'].user:
            raise ValidationError("UserLeagueStatus user can only be defined on creation/must be with current user")
        return user

    def validate(self, validated_data):
        user = validated_data.get('user', None)
        league = validated_data.get('league', None)
        if UserLeagueStatus.objects.filter(user=user, league=league).exists():
            raise ValidationError("this user/league combo already exists, cannot create")
        return validated_data

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        league = validated_data.pop('league', None)
        if not user or not league:
            raise ValidationError('missing parameters')
        return UserLeagueStatus.objects.create(
            user = user,
            league = league,
            request_status = 'pending',
            max_casts = league.default_max_casts,
            max_backups = league.default_max_backups
        )


class UserLeagueStatusRetrieveSerializer(serializers.ModelSerializer):
    user = UserProfilePublicSerializer(many=False, read_only=True)
    league = LeaguePublicSerializer(many=False, read_only=True)
    division_visibilities = serializers.SerializerMethodField()

    class Meta:  # have to redefine Meta since division_visibilities is a new field
        model = UserLeagueStatus
        fields = ('pk', 'user', 'league', 'date_pending', 'date_joined',
                    'request_status', 'max_casts', 'max_backups', 'visibilities', 'division_visibilities')
        read_only_fields = ('pk', 'date_pending')

    def get_division_visibilities(self, instance):
        division_visibilities = []
        for visibility in instance.visibilities.all():
            if not visibility.division.pk in division_visibilities:
                division_visibilities.append(visibility.division.pk)
        return division_visibilities


class UserLeagueStatusUpdateSerializer(UserLeagueStatusBaseSerializer):
    create_only_fields = ('user', 'league')

    def update(self, instance, validated_data):
        for field in self.create_only_fields:
            validated_data.pop(field, None)
        return super().update(instance, validated_data)
