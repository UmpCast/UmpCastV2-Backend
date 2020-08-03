from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .role import RoleRetrieveSerializer
from leagues.models import Division

class DivisionBaseSerializer(serializers.ModelSerializer):
    roles = RoleRetrieveSerializer(source='role_set', many=True, read_only=True)

    class Meta:
        model = Division
        fields = ('pk', 'title', 'league', 'ts_id', 'roles', 'order')
        read_only_fields = ('pk', 'order')
        # create_only_fields = ('league', )


class DivisionCreateSerializer(DivisionBaseSerializer):

    def validate_league(self, league):
        if league in self.context['request'].user.leagues.accepted():
            return league
        else:
            raise ValidationError("Can only create divison for a league you own")


class DivisionRetrieveSerializer(DivisionBaseSerializer):
    pass
