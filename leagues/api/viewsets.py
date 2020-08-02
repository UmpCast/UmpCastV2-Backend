from .serializers.division import (
    DivisionCreateSerializer, DivisionRetrieveSerializer
)

from .serializers.league import (
    LeaguePrivateSerializer, LeaguePublicSerializer
)

from .serializers.role import (
    RoleCreateSerializer, RoleRetrieveSerializer
)

from .serializers.level import (
    LevelCreateSerializer, LevelRetrieveSerializer, LevelUpdateSerializer
)

from .permissions import (
    IsRoleOwner, IsDivisionOwner,
    IsUmpireOwner, IsLeagueOwner, IsLevelOwner,
    LevelListQueryRequired
)

from backend.permissions import (
    IsSuperUser, ActionBasedPermission, IsManager
)

from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
from drf_multiple_serializer import ActionBaseSerializerMixin
from ..models import League, Division, Role, Level
from django.urls import reverse
from rest_framework.decorators import action
from backend.mixins import MoveOrderedModelMixin


class LevelViewSet(ActionBaseSerializerMixin, MoveOrderedModelMixin, mixins.CreateModelMixin,
                        mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    Provide Create, Destroy, List, List-filter functionality for Level model

    create: Create Level \n
    * Permissions: IsManager
    * Extra Validations:
        * Must be owner of league and roles the level is linked to

    update: Update Level \n
    * Permissions: IsLevelOwner

    partial_update: Partial Update Level \n
    * Permissions: IsLevelOwner

    destroy: Destroy Level \n
    * Permissions: IsLevelOwner

    list: List Level \n
    * Permissions: LevelListQueryRequired. The league filter field must be provided and the user must be in the league

    move: Change Level Ordering \n
    * Permissions: IsLevelOwner
    * Extra Validations:
        * "order" field is required
        * "order" value must be within valid range
    * Extra Notes:
        * Ignore below, order is only required field. "order" is 0 indexed, and the level will move to the specified order index
    """

    queryset = Level.objects.all()
    serializer_classes = {
        'default': LevelRetrieveSerializer,
        'create': LevelCreateSerializer,
        'update': LevelUpdateSerializer,
        'partial_update': LevelUpdateSerializer
    }
    filter_fields = ('league', )
    permission_classes = (IsSuperUser | (permissions.IsAuthenticated & ActionBasedPermission),)
    action_permissions = {
        IsManager: ['create'],  # league/roles validated on serializer level
        IsLevelOwner: ['move', 'update', 'partial_update', 'destroy'],
        LevelListQueryRequired: ['list']
    }

    # move orders
    move_filter_variable = 'league'
    move_filter_value = 'league'


class RoleViewSet(ActionBaseSerializerMixin, MoveOrderedModelMixin,
                    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Provide Create/Destroy functionality for Roles

    create: Create Role \n
    * Permissions: IsManager
    * Extra Validations:
        * Must be owner of league the role is linked to

    destroy: Destroy Role \n
    * Permissions: IsRoleOwner

    move: Change Role Ordering \n
    * Permissions: IsRoleOwner
    * Extra Validations:
        * "order" field is required
        * "order" value must be within valid range
    * Extra Notes:
        * Ignore below, order is only required field. "order" is 0 indexed, and the level will move to the specified order index
    """

    queryset = Role.objects.all()
    serializer_classes = {
        'default': RoleRetrieveSerializer,
        'create': RoleCreateSerializer
    }
    permission_classes = (IsSuperUser | (permissions.IsAuthenticated & ActionBasedPermission), )
    action_permissions = {
        IsManager: ['create'],  # league validated on serializer level
        IsRoleOwner: ['move', 'destroy']
    }

    # move orders
    move_filter_variable = 'division'
    move_filter_value = 'division'


class DivisionViewSet(ActionBaseSerializerMixin, MoveOrderedModelMixin,
                        mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Provide Create/Destroy functionality for Divisions

    create: Create Division \n
    * Permissions: IsManager
    * Extra Validations:
        * Must be owner of league the division is linked to

    destroy: Destroy Division \n
    * Permissions: IsDivisionOwner

    move: Change Division Ordering \n
    * Permissions: IsDivisionOwner
    * Extra Validations:
        * "order" field is required
        * "order" value must be within valid range
    * Extra Notes:
        * Ignore below, order is only required field. "order" is 0 indexed, and the level will move to the specified order index
    """

    queryset = Division.objects.all()
    serializer_classes = {
        'default': DivisionRetrieveSerializer,
        'create': DivisionCreateSerializer
    }
    permission_classes = (IsSuperUser | (permissions.IsAuthenticated & ActionBasedPermission), )
    action_permissions = {
        IsManager: ['create'],  # league validated on serializer level
        IsDivisionOwner: ['move', 'destroy']
    }

    # move orders
    move_filter_variable = 'league'
    move_filter_value = 'league'


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
    permission_classes = (IsSuperUser | (permissions.IsAuthenticated & ActionBasedPermission), )
    action_permissions = {
        IsManager: ['create'],
        IsUmpireOwner: ['list'],
        IsLeagueOwner: ['update', 'partial_update', 'retrieve', 'destroy']
    }
