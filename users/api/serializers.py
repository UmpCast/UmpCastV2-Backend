from rest_framework import serializers
from ..models import User
from rest_framework.serializers import ValidationError


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def create(self, validated_data):
        # add validation
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        password = validated_data.get('password')
        return User.objects.create_user(email, first_name, last_name, password)

        # data = self.request.data
        # first_name = data['first_name']
        # last_name = data['last_name']
        # email = data['email']
        # password = data['password']
        # password2 = data['password2']
        #
        # if password != password2:
        #     return Response({'error': 'Passwords do not match!'})
        #
        # if User.objects.filter(email=email).exists():
        #     return Response({'error': 'Email already exists!'})
        # else:
        #     User.objects.create_user(email, first_name, last_name, password)
        #     return Response({'success': 'User created successfully'})

        pass

    def update(self, instance, validated_data):
        pass
