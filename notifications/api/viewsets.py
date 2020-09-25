from .serializers import (
    UmpCastNotificationSerializer, LeagueNotificationSerializer,
    GameNotificationSerializer, ApplicationNotificationSerializer
)

from ..models import (
    UmpCastNotification, LeagueNotification, GameNotification, ApplicationNotification
)

from .filters import (
    UmpCastNotificationFilter, LeagueNotificationFilter, GameNotificationFilter, ApplicationNotificationFilter
)

from backend.permissions import (
    ActionBasedPermission, IsManager, IsSuperUser
)

from .permissions import (
    InLeague, InGameLeague, FilterUserOwner, InFilterLeague, IsApplicationNotificationOwner
)

from rest_framework import viewsets, permissions, mixins


class UmpCastNotificationViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = UmpCastNotification.objects.all()
    serializer_class = UmpCastNotificationSerializer
    filterset_class = UmpCastNotificationFilter
    permission_classes = (permissions.IsAuthenticated, )


class LeagueNotificationViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                                mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = LeagueNotification.objects.all()
    serializer_class = LeagueNotificationSerializer
    filterset_class = LeagueNotificationFilter
    permission_classes = (IsSuperUser | (
        permissions.IsAuthenticated & ActionBasedPermission),)
    action_permissions = {
        IsManager & InLeague: ['update', 'destroy'],
        IsManager: ['create'],  # handle league validation on serializer
        InLeague: ['retrieve'],
        InFilterLeague | FilterUserOwner: ['list']
    }


class GameNotificationViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GameNotification.objects.all()
    serializer_class = GameNotificationSerializer
    filterset_class = GameNotificationFilter
    permission_classes = (IsSuperUser | (
        permissions.IsAuthenticated & ActionBasedPermission),)
    action_permissions = {
        InGameLeague: ['retrieve'],
        FilterUserOwner: ['list']
    }


class ApplicationNotificationViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ApplicationNotification.objects.all()
    serializer_class = ApplicationNotificationSerializer
    filterset_class = ApplicationNotificationFilter
    permission_classes = (IsSuperUser | (
        permissions.IsAuthenticated & ActionBasedPermission),)
    action_permissions = {
        IsApplicationNotificationOwner: ['retrieve'],
        FilterUserOwner: ['list']
    }
