from games.models import Post
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .application import ApplicationRetrieveSerializer


class PostSerializer(serializers.ModelSerializer):
    applications = ApplicationRetrieveSerializer(source='application_set', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('pk', 'role', 'game', 'notes', 'applications')
        read_only_fields = ('pk', )

    def validate_game(self, game):
        if game.division.league not in self.context['request'].user.leagues.accepted():
            raise ValidationError("can only create post for a game in a league you are a manager for")
        return game
