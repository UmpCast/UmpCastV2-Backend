from rest_framework import serializers
from rest_framework.serializers import ValidationError
from users.models import User
from .base import UserProfilePrivateBaseSerializer


class UserProfilePublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'profile_picture', 'date_joined', 'account_type')
        read_only_fields = ('pk', 'first_name', 'last_name', 'profile_picture', 'date_joined', 'account_type')


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
                raise ValidationError("must provide password2 when updating password")
            instance.set_password(validated_data.pop('password'))
        instance.save()
        return super().update(instance, validated_data)
