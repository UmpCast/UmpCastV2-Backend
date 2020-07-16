from rest_framework import serializers
from ..models import User, UserLeagueStatus
from rest_framework.serializers import ValidationError
from leagues.api.serializers import LeaguePublicSerializer
import django.contrib.auth.password_validation as validators
from leagues.models import League

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

    def create(self, validated_data):
        print(validated_data)

        first = validated_data.pop('first_name', None)
        last = validated_data.pop('last_name', None)
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2', None)
        if not (first and last and email and password and password2):
            raise ValidationError("missing parameters")
        if password != password2:
            raise ValidationError("passwords don't match")
        return User.objects.create_user(email, first, last, password)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        instance.save()
        return super().update(instance, validated_data)


class UserLeagueStatusCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLeagueStatus
        fields = ('pk', 'user', 'league', 'date_pending', 'date_joined', 'join_status', 'max_casts')
        read_only_fields = ('pk', 'date_pending')

    def validate_user(self, user):
        if user != self.context['request'].user:
            raise ValidationError("Can only create UserLeagueStatus using current user")
        return user


class UserLeagueStatusUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLeagueStatus
        fields = ('pk', 'user', 'league', 'date_pending', 'date_joined', 'join_status', 'max_casts')
        read_only_fields = ('pk', 'user', 'league', 'date_pending')
