from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        password2 = data['password2']

        if password != password2:
            return Response({'error': 'Passwords do not match!'})

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists!'})
        else:
            User.objects.create_user(email, first_name, last_name, password)
            return Response({'success': 'User created successfully'})





