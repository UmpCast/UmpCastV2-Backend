from rest_framework import serializers
from ..models import League, Division, Role


class LeaguePrivateSerializer(serializers.ModelSerializer):

    class Meta:
        model = League
        fields = ('pk', 'title', 'description', 'league_picture', 'public_access',
                  'date_joined', 'expiration_date', 'adv_scheduling_limit', 'ts_id', 'opponent_library')
        read_only_fields = ('pk', 'date_joined')


class LeaguePublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = League
        fields = ('pk', 'title', 'description', 'league_picture')
        read_only_fields = ('pk',)

# 
# class DivisionPrivateSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Division
#         fields = ('pk', 'title', 'league', 'ts_id')
#         read_only_fields = ('pk', )
#
#
# class DivisionPublicSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Division
#         fields = ('pk', 'title', 'league')
#         read_only_fields = ('pk',)
#
#
# class RoleSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Role
#         fields = ('pk', 'title', 'division')
#         read_only_fields = ('pk')
