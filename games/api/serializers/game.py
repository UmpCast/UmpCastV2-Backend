from rest_framework import serializers
from games.models import Game
from .post import PostSerializer


class GameSerializer(serializers.ModelSerializer):
    posts = PostSerializer(source='post_set', many=True, read_only=True)

    class Meta:
        model = Game
        fields = ('pk', 'title', 'division', 'posts', 'date_time', 'is_active', 'location', 'description')
        read_only_fields = ('pk', )
