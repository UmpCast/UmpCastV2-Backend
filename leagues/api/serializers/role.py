from leagues.models import Role
from rest_framework.serializers import ValidationError
from rest_framework import serializers


class RoleBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ('pk', 'title', 'division', 'order')
        read_only_fields = ('pk', 'order')
        # create_only_fields = ('division',)

class RoleCreateSerializer(RoleBaseSerializer):

    def validate_division(self, division):
        if division.league in self.context['request'].user.leagues.accepted():
            return division
        else:
            raise ValidationError("Can only create role for a league you own")


class RoleRetrieveSerializer(RoleBaseSerializer):
    pass
