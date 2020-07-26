from .serializers import (
    LeaguePrivateSerializer,
    LeaguePublicSerializer,
    DivisionSerializer,
    RoleSerializer,
    LevelSerializer
)

from .permissions import (
    IsManager, IsRoleOwner, IsDivisionOwner,
    IsUmpireOwner, IsLeagueOwner, IsLevelOwner,
    LevelListQueryRequired
)

from backend.permissions import (
    IsSuperUser, ActionBasedPermission
)

from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
from drf_multiple_serializer import ActionBaseSerializerMixin
from ..models import League, Division, Role, Level
from django.urls import reverse
from rest_framework.decorators import action


class LevelViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Provide Create, Destroy, List, List-filter functionality for Level model

    create: Create Level \n
    * Permissions: IsManager
    * Extra Validations:
        * Must be owner of league and roles the level is linked to

    destroy: Destroy Level \n
    * Permissions: IsLevelOwner

    list: List Level \n
    * Permissions: LevelListQueryRequired. The league filter field must be provided and the user must be in the league

    move_level: Change Level Ordering \n
    * Permissions: IsLevelOwner
    * Extra Validations:
        * "order" field is required
        * "order" value must be within valid range
    * Extra Notes:
        * Ignore below, order is only required field. "order" is 0 indexed, and the level will move to the specified order index
    """

    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    filter_fields = ('league', )
    permission_classes = (IsSuperUser | ActionBasedPermission,)
    action_permissions = {
        IsManager: ['create'],  # league/roles validated on serializer level
        IsLevelOwner: ['move_level', 'destroy'],
        LevelListQueryRequired: ['list']
    }

    @action(detail=True, methods=['patch'])
    def move_level(self, request, pk):
        level = self.get_object()
        level_set = Level.objects.filter(league=level.league)
        order = int(request.data.get('order', None))
        if order is None:
            return Response({"error": "missing parameters"}, status=status.HTTP_400_BAD_REQUEST)
        if order < level_set.get_min_order() or order > level_set.get_max_order():
            return Response({"order": "order value out of range"}, status=status.HTTP_400_BAD_REQUEST)
        level.to(order)
        return Response(status=status.HTTP_200_OK)



class RoleViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Provide Create/Destroy functionality for Roles

    create: Create Role \n
    * Permissions: IsManager
    * Extra Validations:
        * Must be owner of league the role is linked to

    destroy: Destroy Role \n
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
