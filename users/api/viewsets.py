from ..models import User, UserLeagueStatus
from .serializers import (
    UserProfilePublicSerializer,
    UserProfilePrivateSerializer,
    UserLeagueStatusCreateSerializer,
    UserLeagueStatusUpdateSerializer
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
    Views for Creating Users, Retrieving Users, and Updating Users
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
    Views for CRUD, Listing, Filtering UserLeagueStatus
    """
    queryset = UserLeagueStatus.objects.all()
    filter_fields = ('user',)

    serializer_classes = {
        'default': UserLeagueStatusCreateSerializer,
        'update': UserLeagueStatusUpdateSerializer,
        'partial_update': UserLeagueStatusUpdateSerializer
    }

    permission_classes = (IsSuperUser | ActionBasedPermission,)
    action_permissions = {
        permissions.IsAuthenticated: ['create', 'list'],  # user restriction enforced on serializer level
        IsUserLeagueStatusOwner: ['retrieve', 'update', 'partial_update', 'destroy'],
    }
