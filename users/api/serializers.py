from rest_framework import serializers
from ..models import User, UserLeagueStatus
from rest_framework.serializers import ValidationError
from leagues.api.serializers import LeaguePublicSerializer
import django.contrib.auth.password_validation as validators
from leagues.models import League
import re

from django.contrib.auth import get_user_model
User = get_user_model()


class UserProfilePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'profile_picture', 'date_joined', 'account_type')
        read_only_fields = ('pk', 'first_name', 'last_name', 'profile_picture', 'date_joined', 'account_type')


class UserProfilePrivateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('pk', 'account_type', 'leagues', 'email', 'email_notifications',
                  'first_name', 'last_name', 'is_configured',
                  'phone_number', 'phone_notifications', 'profile_picture',
                  'date_joined', 'password', 'password2')
        read_only_fields = ('pk',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, password):
        validators.validate_password(password=password)
        return password

    def validate_password2(self, password2):
        if self.initial_data.get('password', None) != password2:
            raise ValidationError('passwords must be equal')
        return password2

    def validate_phone_number(self, phone_number):
        if len(phone_number) != 10:
            raise ValidationError('invalid phone_number length')
        pattern = re.compile("^([0-9]+)+$")
        if not pattern.match(phone_number):
            raise ValidationError('phone numbers can only contain numeric values')
        return phone_number

    def create(self, validated_data):
        first = validated_data.pop('first_name', None)
        last = validated_data.pop('last_name', None)
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2', None)
        if not (first and last and email and password and password2):
            raise ValidationError("missing parameters")
        user = User.objects.create_user(email, first, last, password)
        return self.update(user, validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        instance.save()
        return super().update(instance, validated_data)

class UserLeagueStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLeagueStatus
        fields = ('pk', 'user', 'league', 'date_pending', 'date_joined', 'request_status', 'max_casts', 'visibilities')
        read_only_fields = ('pk', 'date_pending', 'visibilities')
        create_only_fields = ('user', 'league')

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        league = validated_data.pop('league', None)
        if not (user and league):
            raise ValidationError("missing parameters")
        return UserLeagueStatus.objects.create(user=user, league=league)

    def update(self, instance, validated_data):  # remove create_only_fields from dictionary
        for field in UserLeagueStatusSerializer.Meta.create_only_fields:
            validated_data.pop(field, None)
        return super().update(instance, validated_data)

    def validate_user(self, user):
        if user != self.context['request'].user:
            raise ValidationError("UserLeagueStatus user can only be defined on creation/must be with current user")
        return user

    def validate(self, validated_data):
        user = validated_data.get('user', None)
        league = validated_data.get('league', None)
        if UserLeagueStatus.objects.filter(user=user, league=league).exists():
            raise ValidationError("this user/league combo already exists, cannot create")
        return validated_data
