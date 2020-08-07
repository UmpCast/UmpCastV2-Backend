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
    IsApplicationLeague, IsPostLeague, IsGameLeague, GameFilterPermissions,
    ListByDivisionPermission, ApplicationFilterPermission
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
from rest_framework.decorators import action
from .filters import GameFilter


class ApplicationViewSet(MoveOrderedModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                            mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Provide Create, Destroy, Move functionality for ordered Application

    create: Create Application \n
    * Permissions: IsManager (of league application is assigned to)

    destroy: Destroy Application \n
    * Permissions: IsManager (of league application is assigned to)

    list: List/Filter Application \n
    * Permissions: ApplicationFilterPermission
        * User Filter-Param is required
        * User must be same as request user

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
        ApplicationFilterPermission: ["list"]
    }
    filter_fields = ('user',)

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
    * Permission: GameFilterPermission (Can only filter division if accepted to respective league, cannot list all games)
    * Query Params:
        * Division (required)
        * Date_time_before (iso format)
        * Date_time_after (iso format)

    list_by_division: List By Divisions \n
    * Permission: Request User must be in the league of each division requested
    * Extra Notes:
        * Divisions passed in list over division pk's. Any game in any division is added
        * Result follows pagination rules
    """
    serializer_class = GameSerializer
    permission_classes = (IsSuperUser | (permissions.IsAuthenticated & ActionBasedPermission),)
    action_permissions = {
        IsManager: ["create"],  # manager of league requirement enforced on serializer level
        IsGameLeague: ["retrieve"],
        IsManager & IsGameLeague: ["destroy"],
        GameFilterPermissions: ["list"],
        ListByDivisionPermission: ["list_by_division"]
    }

    queryset = Game.objects.all()
    filterset_class = GameFilter

    @action(detail=False, methods=['post'])
    def list_by_division(self, request):
        division_list = request.data.get('divisions', None)
        qs = Game.objects.none()
        for division in division_list:
            qs = qs | Game.objects.filter(division__pk=division)
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
