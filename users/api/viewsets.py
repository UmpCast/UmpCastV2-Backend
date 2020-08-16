from ..models import User, UserLeagueStatus

from .serializers.user import (
    UserProfilePublicSerializer, UserProfilePrivateCreateSerializer,
    UserProfilePrivateRetrieveSerializer, UserProfilePrivateUpdateSerializer
)

from .serializers.userleaguestatus import (
    UserLeagueStatusCreateSerializer, UserLeagueStatusRetrieveSerializer, UserLeagueStatusUpdateSerializer
)

from .permissions import (
    IsLeagueMember, IsUserOwner,
    IsUserLeagueStatusManager, IsUserLeagueStatusOwner, UserLeagueStatusFilterPermission
)

from .filters import (
    UserLeagueStatusFilter
)

from rest_framework import viewsets, mixins, permissions, status
from drf_multiple_serializer import ActionBaseSerializerMixin
from backend.permissions import (
    ActionBasedPermission,
    IsSuperUser
)
from rest_framework.decorators import action
from leagues.models import Level
from rest_framework.response import Response


class UserViewSet(ActionBaseSerializerMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Provide Create, Retrieve, Update, List, List-Filter functionality for User

    create: Create User \n
    * Permissions: AllowAny
    * Extra Validation:
        * Valid Email
        * Valid Password
        * Matching passwords
        * Phone Number Length/Numeric Only

    retrieve: Retrieve User \n
    * Permissions: IsUserOwner
    * Extra Notes:
        * Get current user using pk='me'

    update: Full Update User \n
    * Permissions: IsUserOwner

    partial_update: Partial Update User \n
    * Permissions: IsUserOwner

    list: List User \n
    * Permissions: IsUserOwner (if using user query param)
    * Query Params: Leagues, Account_type
    """

    queryset = User.objects.all()
    filter_fields = ('leagues', 'account_type')

    serializer_classes = {
        'default': UserProfilePrivateRetrieveSerializer,
        'create': UserProfilePrivateCreateSerializer,
        'update': UserProfilePrivateUpdateSerializer,
        'partial_update': UserProfilePrivateUpdateSerializer,
        'list': UserProfilePublicSerializer
    }

    permission_classes = (IsSuperUser | ActionBasedPermission,)
    action_permissions = {
        permissions.AllowAny: ['create'],
        permissions.IsAuthenticated & IsLeagueMember: ['list'],
        permissions.IsAuthenticated & IsUserOwner: ['update', 'partial_update', 'retrieve'],
    }

    def get_object(self):  # custom get object for /me endpoint
        pk = self.kwargs.get('pk', None)
        if pk == 'me':
            return self.request.user
        return super().get_object()


class UserLeagueStatusViewSet(ActionBaseSerializerMixin, viewsets.ModelViewSet):
    """
    Provide CRUD, List, List-Filter functionality for UserLeagueStatus

    create: Create UserLeagueStatus \n
    * Permissions: IsAuthenticated
    * Extra Validations:
        * Can only create UserLeagueStatus using current user
        * There can only exist one User/League pair
        * Only user/league can be specified (other update operations restricted to manager)

    retrieve: Retrieve UserLeagueStatus \n
    * Permissions: IsUserLeagueStatusOwner or IsUserLeagueStatusManager

    update: Full Update UserLeagueStatus \n
    * Permissions: IsUserLeagueStatusManager

    partial_update: Partial Update UserLeagueStatus \n
    * Permissions: IsUserLeagueStatusManager

    destroy: Destroy UserLeagueStatus \n
    * Permissions: IsUserLeagueStatusOwner or IsUserLeagueStatusManager

    list: List UserLeagueStatus \n
    * Permissions: UserLeagueStatusFilterPermission
        * Umpires must filter by current user. League or no league is optional.
        * Managers can both apply to leagues and manage leagues. Permissions filtered accordingly
    * Query Params: User, League, Request_status, Account_Type
    * Extra Notes:
        * Account_type is filtered using the user__account_type lookup expression

    apply_level: Apply a Level to UserLeagueStatus \n
    * Permissions: Owner of Applied Level
    * Extra Notes:
        * Ignore below. The only required post field is "level", the pk of the level object
    """
    queryset = UserLeagueStatus.objects.all()
    filterset_class = UserLeagueStatusFilter

    serializer_classes = {
        'default': UserLeagueStatusRetrieveSerializer,
        'create': UserLeagueStatusCreateSerializer,
        'update': UserLeagueStatusUpdateSerializer,
        'partial_update': UserLeagueStatusUpdateSerializer
    }

    permission_classes = (IsSuperUser | (permissions.IsAuthenticated & ActionBasedPermission),)
    action_permissions = {
        permissions.IsAuthenticated: ['create'],  # user restriction enforced on serializer level
        UserLeagueStatusFilterPermission: ['list'],
        IsUserLeagueStatusOwner | IsUserLeagueStatusManager: ['retrieve', 'destroy'],
        IsUserLeagueStatusManager: ['apply_level', 'update', 'partial_update'],
    }

    @action(detail=True, methods=['post'])
    def apply_level(self, request, pk):
        uls = self.get_object()
        uls.visibilities.clear()
        level_pk = request.data.get('level', None)
        if level_pk is None:
            return Response({"error": "missing parameters"}, status=status.HTTP_400_BAD_REQUEST)
        if not Level.objects.filter(pk=level_pk).exists():
            return Response({"level": ["invalid level pk"]}, status=status.HTTP_400_BAD_REQUEST)
        level_obj = Level.objects.get(pk=level_pk)
        if level_obj.league != uls.league:  # permissions inherently checks if manager owns level
            return Response({"level": ["level from one league cannot be applied to uls of another league"]}, status=status.HTTP_400_BAD_REQUEST)
        for role in level_obj.visibilities.all():
            uls.visibilities.add(role)
        return Response(status=status.HTTP_200_OK)
