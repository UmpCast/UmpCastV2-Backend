from rest_framework.serializers import ValidationError
from leagues.models import Level
from rest_framework import serializers


class LevelBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Level
        fields = ('pk', 'title', 'league', 'visibilities', 'order')
        read_only_fields = ('pk', 'order')


class LevelCreateSerializer(LevelBaseSerializer):

    def validate(self, data):
        if 'visibilities' in data:
            for visibility in data['visibilities']:
                if visibility.division.league != data['league']:
                    raise ValidationError(
                        'roles in visibilities for level must be from league')
        if data['league'].level_set.filter(title=data['title']).exists():
            raise ValidationError('duplicate title for level in league')
        return super().validate(data)

    def validate_league(self, league):
        if league in self.context['request'].user.leagues.accepted():
            return league
        else:
            raise ValidationError(
                "League can only be specified on creation/must be with a owned league")


class LevelRetrieveSerializer(LevelBaseSerializer):
    pass


class LevelUpdateSerializer(LevelBaseSerializer):
    create_only_fields = ('league', )

    def update(self, instance, validated_data):  # remove create_only_fields from dictionary
        for field in self.create_only_fields:
            validated_data.pop(field, None)
        if 'visibilities' in validated_data:
            for visibility in validated_data['visibilities']:
                if visibility.division.league != instance.league:
                    raise ValidationError(
                        'roles in visibilities from wrong league added to level')
        if 'title' in validated_data:
            if instance.league.level_set.filter(title=validated_data['title']).exists():
                raise ValidationError('duplicate title for level in league')
        return super().update(instance, validated_data)
