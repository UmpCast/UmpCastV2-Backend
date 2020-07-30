from users.models import UserLeagueStatus
from rest_framework.serializers import ValidationError
from leagues.api.serializers import LeaguePublicSerializer
from users.api.serializers.user import UserProfilePublicSerializer
from .base import UserLeagueStatusBaseSerializer


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


class UserLeagueStatusRetrieveSerializer(UserLeagueStatusBaseSerializer):
    user = UserProfilePublicSerializer(many=False, read_only=True)
    league = LeaguePublicSerializer(many=False, read_only=True)


class UserLeagueStatusUpdateSerializer(UserLeagueStatusBaseSerializer):
    create_only_fields = ('user', 'league')

    def update(self, instance, validated_data):
        for field in self.create_only_fields:
            validated_data.pop(field, None)
        return super().update(instance, validated_data)
