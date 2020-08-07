from rest_framework import serializers
from games.models import Application
from rest_framework.serializers import ValidationError
from users.api.serializers.user import UserProfilePublicSerializer


class ApplicationBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('pk', 'post', 'user', 'comments', 'order')
        read_only_fields = ('pk', 'order')


class ApplicationCreateSerializer(ApplicationBaseSerializer):
    def validate_user(self, user):
        if not user.is_manager() and user != self.context['request'].user:
            raise ValidationError("must either be the requesting user, or a manager")
        return user

    def validate_post(self, post):
        if post.game.division.league not in self.context['request'].user.leagues.accepted():
            raise ValidationError("can only create application for a post in a league you are a manager for")
        return post

    def validate(self, validated_data):
        post = validated_data.get('post', None)
        user = validated_data.get('user', None)
        if post.game.division.league not in user.leagues.accepted():
            raise ValidationError("cannot add this user to this post due to league restrictions")
        if Application.objects.filter(post=post, user=user).exists():  # user can only create
            raise ValidationError("already applied to this post!")
        if Application.objects.filter(post__game=post.game, user=user).exists():
            raise ValidationError("already applied to this game!")
        return super().validate(validated_data)


class ApplicationRetrieveSerializer(ApplicationBaseSerializer):
    user = UserProfilePublicSerializer(many=True, read_only=True)
