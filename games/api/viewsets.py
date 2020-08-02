from .serializers.application import (
    ApplicationSerializer
)

from .serializers.game import (
    GameSerializer
)

from .serializers.post import (
    PostSerializer
)

from .permissions import (
    IsApplicationLeague, IsPostLeague, IsGameLeague
)

from backend.permissions import (
    IsManager
)

from backend.permissions import (
    ActionBasedPermission,
    IsSuperUser
)

from backend.mixins import (
    MoveOrderedModelMixin
)

from rest_framework import viewsets, permissions, mixins, status
from ..models import Application, Post, Game
import django_filters
from rest_framework.decorators import action


class ApplicationViewSet(MoveOrderedModelMixin, mixins.CreateModelMixin,
                            mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (IsSuperUser | (permissions.IsAuthenticated & ActionBasedPermission),)
    action_permissions = {
        IsManager: ["create"], # manager of league requirement enforced on serializer level
        IsManager & IsApplicationLeague: ["destroy", "move"],
    }

    # move orders
    move_filter_variable = 'post'
    move_filter_value = 'post'


class PostViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsSuperUser | (permissions.IsAuthenticated & ActionBasedPermission),)
    action_permissions = {
        IsManager: ["create"],  # manager of league requirement enforced on serializer level
        IsManager & IsPostLeague: ["destroy"]
    }


class GameViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = GameSerializer
    permission_classes = (IsSuperUser | (permissions.IsAuthenticated & ActionBasedPermission),)
    action_permissions = {
        IsManager: ["create"],  # manager of league requirement enforced on serializer level
        IsGameLeague: ["retrieve"],
        IsManager & IsGameLeague: ["destroy"]
    }

    def get_queryset(self):
        queryset = Game.objects.all()
        division_pk = self.request.query_params.get('division', None)
        league_pk = self.request.query_params.get('league', None)
        if division_pk is not None:
            queryset = queryset.filter(division__pk=division_pk)
        if league_pk is not None:
            queryset = queryset.filter(division__league__pk=league_pk)
        return queryset
