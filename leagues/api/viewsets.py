from .serializers import LeaguePrivateSerializer
from rest_framework import viewsets, mixins, permissions
from backend.permissions import ActionBasedPermission
from drf_multiple_serializer import ActionBaseSerializerMixin


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return True if request.user.is_manager() else False


class IsUmpireOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        user_pk = self.request.query_params.get('user', None)
        if user_pk is None:
            return True
        return True if request.user.pk == user_pk else False


class IsLeagueOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        league = League.objects.get(pk=view.kwargs['pk'])
        return True if request.user.is_manager() and request.user.league_set.filter(league=league).exists() else False


class LeagueViewSet(ActionBaseSerializerMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_classes = {
        'default': LeaguePrivateSerializer
    }

    permission_classes = (ActionBasedPermission, )
    action_permissions = {
        IsManager: ['create'],
        IsUmpireOwner: ['list'],
        IsLeagueOwner: ['update', 'partial_update', 'retrieve']
    }

    def get_queryset(self):  # filter queryset based on query-params
        queryset = League.objects.all()
        user_pk = self.request.query_params.get('user', None)
        if user_pk is not None:
            queryset = queryset.filter(user__pk=user_pk)
        return queryset
