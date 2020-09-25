from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from games.models import Application
from users.api.serializers.user import UserProfilePublicSerializer
from users.models import User, UserLeagueStatus


class ApplicationBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('pk', 'post', 'user', 'comments', 'order')
        read_only_fields = ('pk', 'order')


class ApplicationCreateSerializer(ApplicationBaseSerializer):
    def validate_user(self, user):
        if not user.is_manager() and user != self.context['request'].user:
            raise ValidationError(
                "must either be the requesting user, or a manager")
        return user

    def validate_post(self, post):
        if post.game.division.league not in self.context['request'].user.leagues.accepted():
            raise ValidationError(
                "can only create application for a post in a league you are a manager for")
        return post

    def validate(self, validated_data):
        post = validated_data.get('post', None)
        user = validated_data.get('user', None)
        adv_scheduling = post.game.division.league.adv_scheduling_limit
        if (post.game.date_time - timezone.now()).days > adv_scheduling:
            raise ValidationError(
                ' '.join(['cannot apply', str(adv_scheduling), 'days before game']))
        if post.game.division.league not in user.leagues.accepted():
            raise ValidationError(
                "cannot add this user to this post due to league restrictions")
        if not UserLeagueStatus.objects.filter(user=user, league=post.role.division.league).exists():
            raise ValidationError(
                "this error should not occur: user not in relevant league to apply for this game")
        if not user.is_manager() and post.role not in UserLeagueStatus.objects.get(user=user, league=post.role.division.league).visibilities.all():
            raise ValidationError(
                "this error should not occur: user does not have visibility to apply for this post")
        # user can only create
        if Application.objects.filter(post=post, user=user).exists():
            raise ValidationError("already applied to this post!")
        if Application.objects.filter(post__game=post.game, user=user).exists():
            raise ValidationError("already applied to this game!")
        return super().validate(validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['user'] = UserProfilePublicSerializer(
            User.objects.get(pk=ret['user'])).data
        return ret


class ApplicationRetrieveSerializer(ApplicationBaseSerializer):
    user = UserProfilePublicSerializer(many=False, read_only=True)


class ApplicationPublicSerializer(ApplicationBaseSerializer):
    game = serializers.SerializerMethodField()

    def get_game(self, obj):
        return obj.post.game.pk

    class Meta(ApplicationBaseSerializer.Meta):
        fields = ApplicationBaseSerializer.Meta.fields + ('game', )
