from ..models import TeamSnapNote, TeamSnapNoteItem
from rest_framework import serializers


class TeamSnapNoteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamSnapNoteItem
        fields = ('note', )


class TeamSnapNoteSerializer(serializers.ModelSerializer):
    notes = TeamSnapNoteItemSerializer(
        source='teamsnapnoteitem_set', many=True, read_only=True)

    class Meta:
        model = TeamSnapNote
        fields = ('pk', 'league', 'date_time', 'note_type', 'notes')
