from rest_framework import serializers
from rest_framework.serializers import ValidationError
from users.models import User, UserLeagueStatus
import django.contrib.auth.password_validation as validators
import re


class UserProfilePrivateBaseSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('pk', 'account_type', 'leagues', 'email', 'email_notifications',
                  'first_name', 'last_name', 'phone_number', 'phone_notifications', 'profile_picture',
                  'date_joined', 'password', 'password2')
        read_only_fields = ('pk', 'leagues')
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


class UserLeagueStatusBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLeagueStatus
        fields = ('pk', 'user', 'league', 'date_pending', 'date_joined',
                    'request_status', 'max_casts', 'max_backups', 'visibilities')
        read_only_fields = ('pk', 'date_pending')
