from ..models import TeamSnapNote
from rest_framework import serializers


class TeamSnapNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamSnapNote
        fields = ('pk', 'notes', 'league', 'date_time')