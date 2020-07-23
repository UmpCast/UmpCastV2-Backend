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
from rest_framework import viewsets, mixins, permissions
from drf_multiple_serializer import ActionBaseSerializerMixin
from backend.permissions import (
    ActionBasedPermission,
    IsSuperUser
)


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

# TODO: List needs updating
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
    * THIS IS STILL IN PROGRESS!
    * Permissions: IsAuthenticated
    * Query Params: User
    """
    queryset = UserLeagueStatus.objects.all()
    filter_fields = ('user',)
    serializer_class = UserLeagueStatusSerializer
    permission_classes = (IsSuperUser | ActionBasedPermission,)
    action_permissions = {
        permissions.IsAuthenticated: ['create', 'list'],  # user restriction enforced on serializer level
        IsUserLeagueStatusOwner: ['retrieve', 'update', 'partial_update', 'destroy'],
    }
