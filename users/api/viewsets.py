from ..models import User, UserLeagueStatus
from .serializers import (
    UserProfilePublicSerializer,
    UserProfilePrivateSerializer,
    UserLeagueStatusSerializer
)
from .permissions import (
    IsLeagueMember, IsUserOwner,
    IsUserLeagueStatusOwner
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
        'default': UserProfilePrivateSerializer,
        'list': UserProfilePublicSerializer
    }

    permission_classes = (IsSuperUser | ActionBasedPermission,)
    action_permissions = {
        permissions.AllowAny: ['create'],
        IsLeagueMember: ['list'],
        IsUserOwner: ['update', 'partial_update', 'retrieve'],
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

    retrieve: Retrieve UserLeagueStatus \n
    * Permissions: IsUserLeagueStatusOwner

    update: Full Update UserLeagueStatus \n
    * Permissions: IsUserLeagueStatusOwner

    partial_update: Partial Update UserLeagueStatus \n
    * Permissions: IsUserLeagueStatusOwner

    destroy: Destroy UserLeagueStatus \n
    * Permissions: IsUserLeagueStatusOwner

    list: List UserLeagueStatus \n
    * Permissions: IsAuthenticated (only user pk is provided, no private info)
    * Query Params: User, League

    apply_level: Apply a Level to UserLeagueStatus \n
    * Permissions: Owner of Applied Level
    * Extra Notes:
        * Ignore below. The only required post field is "level", the pk of the level object
    """
    queryset = UserLeagueStatus.objects.all()
    filter_fields = ('user', 'league')
    serializer_class = UserLeagueStatusSerializer
    permission_classes = (IsSuperUser | ActionBasedPermission,)
    action_permissions = {
        permissions.IsAuthenticated: ['create', 'list', 'apply_level'],  # user restriction enforced on serializer level
        IsUserLeagueStatusOwner: ['retrieve', 'update', 'partial_update', 'destroy'],
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
        if level_obj.league not in request.user.leagues.all():
            return Response({"level": ["you are not the owner of this level"]}, status=status.HTTP_400_BAD_REQUEST)
        for role in level_obj.roles.all():
            uls.visibilities.add(role)
        return Response(status=status.HTTP_200_OK)
