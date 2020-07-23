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
    """
    Provide Create/Destroy functionality for Roles

    create: Create Role \n
    * Permissions: IsManager
    * Extra Validations:
        * Must be owner of league the role is linked to

    destroy: Destroy Division \n
    * Permissions: IsRoleOwner
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (IsSuperUser | ActionBasedPermission, )
    action_permissions = {
        IsManager: ['create'],  # league validated on serializer level
        IsRoleOwner: ['destroy']
    }


class DivisionViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Provide Create/Destroy functionality for Divisions

    create: Create Division \n
    * Permissions: IsManager
    * Extra Validations:
        * Must be owner of league the division is linked to

    destroy: Destroy Division \n
    * Permissions: IsDivisionOwner
    """

    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    permission_classes = (IsSuperUser | ActionBasedPermission, )
    action_permissions = {
        IsManager: ['create'],  # league validated on serializer level
        IsDivisionOwner: ['destroy']
    }


class LeagueViewSet(ActionBaseSerializerMixin, viewsets.ModelViewSet):
    """
    Provide CRUD, List, List-Filter functionality for League

    create: Create League \n
    * Permissions: IsManager
    * Extra Notes:
        * Manager automatically added to created league

    retrieve: Retrieve League \n
    * Permissions: IsLeagueOwner

    update: Full Update League \n
    * Permissions: IsLeagueOwner

    partial_update: Partial Update League \n
    * Permissions: IsLeagueOwner

    destroy: Destroy League \n
    * Permissions: IsLeagueOwner

    list: List League \n
    * Permissions: IsUmpireOwner (if using user query param)
    * Query Params: User
    """

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
