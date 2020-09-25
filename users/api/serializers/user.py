import re

import django.contrib.auth.password_validation as validators
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from leagues.api.serializers.league import LeaguePublicSerializer, LeaguePrivateSerializer

from users.models import User


class UserProfilePrivateBaseSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=128, write_only=True)
    accepted_leagues = serializers.SerializerMethodField()
    pending_leagues = serializers.SerializerMethodField()
    rejected_leagues = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('pk', 'account_type', 'email', 'email_notifications',
                  'first_name', 'last_name', 'phone_number', 'phone_notifications', 'profile_picture',
                  'date_joined', 'password', 'password2', 'accepted_leagues', 'pending_leagues', 'rejected_leagues',
                  'league_notifications', 'game_notifications', 'application_notifications')
        read_only_fields = ('pk', 'accepted_leagues',
                            'pending_leagues', 'rejected_leagues')
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
            raise ValidationError(
                'phone numbers can only contain numeric values')
        return phone_number

    def get_accepted_leagues(self, instance):
        accepted_leagues = instance.leagues.accepted()
        return LeaguePrivateSerializer(accepted_leagues, many=True).data

    def get_pending_leagues(self, instance):
        pending_leagues = instance.leagues.pending()
        return LeaguePublicSerializer(pending_leagues, many=True).data

    def get_rejected_leagues(self, instance):
        rejected_leagues = instance.leagues.rejected()
        return LeaguePublicSerializer(rejected_leagues, many=True).data


class UserProfilePublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name',
                  'profile_picture', 'date_joined', 'account_type')
        read_only_fields = ('pk', 'first_name', 'last_name',
                            'profile_picture', 'date_joined', 'account_type')


class UserProfilePrivateCreateSerializer(UserProfilePrivateBaseSerializer):

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


class UserProfilePrivateRetrieveSerializer(UserProfilePrivateBaseSerializer):
    pass


class UserProfilePrivateUpdateSerializer(UserProfilePrivateBaseSerializer):

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            if 'password2' not in validated_data:  # password2 must be passed in, validation in validate_password2
                raise ValidationError(
                    "must provide password2 when updating password")
            instance.set_password(validated_data.pop('password'))
        instance.save()
        return super().update(instance, validated_data)
