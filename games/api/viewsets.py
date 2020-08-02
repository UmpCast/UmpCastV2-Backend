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
    IsApplicationLeague, IsPostLeague, IsGameLeague, GameFilterPermissions
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
    """
    Provide Create, Destroy, Move functionality for ordered Application

    create: Create Application \n
    * Permissions: IsManager (of league application is assigned to)

    destroy: Destroy Application \n
    * Permissions: IsManager (of league application is assigned to)

    move: Move Application Order \n
    * Permissions: IsManager (of league application is assigned to)
    * Extra Validations:
        * If order is out of range, will return validation error
    * Extra Notes:
        * pk of application to be moved passed in url
        * order of desired location (only parameter) passed in json body, all other applications will automatically reorder
    """
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
    """
    Provide Create and Destroy functionality for Post Model

    create: Create Post \n
    * Permissions: IsManager (of league post is assigned to)

    destroy: Destroy Post \n
    * Permissions: IsManager (of league post is assigned to)
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsSuperUser | (permissions.IsAuthenticated & ActionBasedPermission),)
    action_permissions = {
        IsManager: ["create"],  # manager of league requirement enforced on serializer level
        IsManager & IsPostLeague: ["destroy"]
    }


class GameViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Provide Create, Retrieve, Destroy, List, List-Filter functionality for Game Model

    create: Create Game \n
    * Permissions: IsManager (of league game is assigned to)

    retrieve: Retreieve Game \n
    * Permissions: IsGameLeague (is a member of the league the game is in)
    * Extra Notes:
        * Returns a list of posts attatched to the game.
        * Each post also contains a list of applications

    destroy: Destroy Game \n
    * Permission: IsManager & IsGameLeague (is a manger and in the league of the game)

    list: List Games \n
    * Permission: GameFilterPermission (Can only filter league/division if accepted to respective league, cannot list all games)
    * Query Params:
        * Division
        * League
    """
    serializer_class = GameSerializer
    permission_classes = (IsSuperUser | (permissions.IsAuthenticated & ActionBasedPermission),)
    action_permissions = {
        IsManager: ["create"],  # manager of league requirement enforced on serializer level
        IsGameLeague: ["retrieve"],
        IsManager & IsGameLeague: ["destroy"],
        GameFilterPermissions: ["list"]
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
