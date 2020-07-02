from ..models import User
from .serializers import UserSerializer
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# from rest_framework.decorators import action
# from rest_framework import renderers


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # def test_view_set(self):
    #     return Response({'deez': 'nuts'})

# class UserViewSet(viewsets.ViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# # @action
#     def deeznuts(self):
#         return Response({'deez':'nuts'})
#
#     def create(self, request):
#         data = request.data
#         serializer = UserSerializer(data=data)
#         if not serializer.is_valid():
#             return Response({'error': 'invalid data format'})
#         serializer.save()
#         response = serializer.data
#         response['success'] = 'user created successfully'
#         return Response(response)
#         # response = serializer.data
#         # if serializer.is_valid():
#         #     serializer.save()
#         #     response['success'] = 'User created successfully'
#         # else:
#         #     response['failied'] = 'User not created successfully'
#         # return Response(response)
#
#     def retrieve(self, request, pk=None):
#         queryset = User.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#
#     def update(self, request, pk=None):
#         return Response({'type':'update'})
#
#     # permission_classes = (ActionBasedPermission,)
#     # action_permissions = {
#     #     IsAuthenticated: ['update', 'partial_update', 'destroy', 'list', 'create'],
#     #     AllowAny: ['retrieve']
#     # }
