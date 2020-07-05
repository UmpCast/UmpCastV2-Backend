from ..models import User
from .serializers import UserProfileSerializer, UserListSerializer
from rest_framework import viewsets, mixins, permissions
from drf_multiple_serializer import ActionBaseSerializerMixin
from backend.permissions import ActionBasedPermission


class IsProfileOwner(permissions.BasePermission):
    """
    Check if request user owns profile
    """
    def has_permission(self, request, view):
        user = User.objects.get(pk=view.kwargs['pk'])
        return True if user == request.user else False


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
        'default': UserProfileSerializer,
        'list': UserListSerializer
    }

    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        permissions.AllowAny: ['create'],
        IsLeagueMember: ['list'],
        IsProfileOwner: ['update', 'partial_update', 'retrieve']
    }

    def get_queryset(self):  # filter queryset based on query-params
        queryset = User.objects.all()
        league_pk = self.request.query_params.get('league', None)
        if league_pk is not None:
            queryset = queryset.filter(leagues__in=league_pk)
        account_type = self.request.query_params.get('account_type', None)
        if account_type is not None:
            queryset = queryset.filter(account_type=account_type)
        return queryset

