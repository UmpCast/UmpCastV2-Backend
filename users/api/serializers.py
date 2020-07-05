from rest_framework import serializers
from ..models import User
from rest_framework.serializers import ValidationError
import django.contrib.auth.password_validation as validators

from django.contrib.auth import get_user_model
User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'profile_picture', 'date_joined', 'account_type')
        read_only_fields = ('pk', 'first_name', 'last_name', 'profile_picture', 'date_joined', 'account_type')


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk', 'account_type', 'leagues', 'email', 'email_notifications',
                  'first_name', 'last_name', 'is_configured',
                  'phone_number', 'phone_notifications', 'profile_picture',
                  'date_joined', 'password')
        read_only_fields = ('pk',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, password):
        validators.validate_password(password=password)
        return password

    def create(self, validated_data):
        first = validated_data.pop('first_name', None)
        last = validated_data.pop('last_name', None)
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        if not (first and last and email and password):
            raise ValidationError("missing parameters")
        return User.objects.create_user(email, first, last, password)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        instance.save()
        return super().update(instance, validated_data)
