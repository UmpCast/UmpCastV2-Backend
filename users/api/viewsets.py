from ..models import User, UserLeagueStatus
from .serializers import (
    UserProfilePublicSerializer,
    UserProfilePrivateSerializer,
    UserLeagueStatusCreateSerializer,
    UserLeagueStatusUpdateSerializer
)
from rest_framework import viewsets, mixins, permissions
from drf_multiple_serializer import ActionBaseSerializerMixin
from backend.permissions import ActionBasedPermission


class IsUserOwner(permissions.BasePermission):
    """
    Check if request user owns profile or is viewing personal profile
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if view.kwargs['pk'] == 'me':
            return True
        user = User.objects.get(pk=view.kwargs['pk'])
        return user == request.user



class IsLeagueMember(permissions.BasePermission):
    """
    Check if request user has valid user-list query scope
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        league_pk = request.query_params.get('league', None)
        if league_pk is not None and request.user.leagues.filter(pk=league_pk).exists():
            return True
        return request.user.is_superuser


class UserViewSet(ActionBaseSerializerMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Views for Creating Users, Retrieving Users, and Updating Users
    """
    serializer_classes = {
        'default': UserProfilePrivateSerializer,
        'list': UserProfilePublicSerializer
    }

    permission_classes = (ActionBasedPermission,)
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


    def get_queryset(self):  # filter queryset based on query-params
# TODO: input format validation
        queryset = User.objects.all()
        league_pk = self.request.query_params.get('league', None)
        if league_pk is not None:
            queryset = queryset.filter(leagues__in=league_pk)
        account_type = self.request.query_params.get('account_type', None)
        if account_type is not None:
            queryset = queryset.filter(account_type=account_type)
        return queryset


class IsUserLeagueStatusOwner(permissions.BasePermission):
    """
    Check if request user is the owner of the UserLeagueStatus
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return UserLeagueStatus.objects.filter(pk=view.kwargs['pk'], user=request.user).exists()


class UserLeagueStatusViewSet(ActionBaseSerializerMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    """
    Views for CRUD, Listing, Filtering UserLeagueStatus
    """
    serializer_classes = {
        'default': UserLeagueStatusCreateSerializer,
        'update': UserLeagueStatusUpdateSerializer,
        'partial_update': UserLeagueStatusUpdateSerializer
    }

    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        permissions.IsAuthenticated: ['create', 'list'],  # user restriction enforced on serializer level
        IsUserLeagueStatusOwner: ['retrieve', 'update', 'partial_update', 'destroy'],
    }

    def get_queryset(self):  # filter queryset based on query-params
        queryset = UserLeagueStatus.objects.all()
        user_pk = self.request.query_params.get('user', None)
# TODO: Input format validation
        if user_pk is not None:
            queryset = queryset.filter(user__pk=user_pk)
        return queryset
