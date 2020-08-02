from rest_framework import serializers
from games.models import Application
from rest_framework.serializers import ValidationError


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ('pk', 'post', 'user', 'comments', 'order')
        read_only_fields = ('pk', 'order')

    def validate_post(self, post):
        if post.game.division.league not in self.context['request'].user.leagues.accepted():
            raise ValidationError("can only create application for a post in a league you are a manager for")
        return post
