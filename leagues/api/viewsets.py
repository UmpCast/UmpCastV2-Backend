from .serializers import (
    LeaguePrivateSerializer,
    LeaguePublicSerializer,
    DivisionSerializer,
    RoleSerializer,
)

from .permissions import (
    IsManager, IsRoleOwner, IsDivisionOwner,
    IsUmpireOwner, IsLeagueOwner
)

from backend.permissions import (
    IsSuperUser, ActionBasedPermission
)

from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
from drf_multiple_serializer import ActionBaseSerializerMixin
from ..models import League, Division, Role
from django.urls import reverse
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class RoleViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (IsSuperUser | ActionBasedPermission, )
    action_permissions = {
        IsManager: ['create'],  # league validated on serializer level
        IsRoleOwner: ['destroy']
    }


class DivisionViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    permission_classes = (IsSuperUser | ActionBasedPermission, )
    action_permissions = {
        IsManager: ['create'],  # league validated on serializer level
        IsDivisionOwner: ['destroy']
    }


class LeagueViewSet(ActionBaseSerializerMixin, viewsets.ModelViewSet):
    queryset = League.objects.all()
    filter_fields = ('user', )
    serializer_classes = {
        'default': LeaguePrivateSerializer,
        'list': LeaguePublicSerializer
    }
    permission_classes = (IsSuperUser | ActionBasedPermission, )
    action_permissions = {
        IsManager: ['create'],
        IsUmpireOwner: ['list'],
        IsLeagueOwner: ['update', 'partial_update', 'retrieve', 'destroy']
    }
