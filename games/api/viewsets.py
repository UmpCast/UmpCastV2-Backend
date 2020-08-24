from .serializers.application import (
    ApplicationCreateSerializer, ApplicationRetrieveSerializer
)

from .serializers.game import (
    GameSerializer
)

from .serializers.post import (
    PostSerializer
)

from .permissions import (
    IsApplicationLeague, IsPostLeague, IsGameLeague, ApplicationFilterPermission,
    GameFilterDivision, GameFilterDivisionIn, GameFilterUser,
    GameFilterDivisionManager, GameFilterDivisionInManager
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
from .filters import GameFilter, ApplicationFilter
from drf_multiple_serializer import ActionBaseSerializerMixin
from django.utils import timezone
from rest_framework.response import Response


class ApplicationViewSet(ActionBaseSerializerMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                         mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Provide Create, Destroy, Move functionality for ordered Application

    create: Create Application \n
    * Permissions: IsManager (of league application is assigned to)
    * Extra Notes:
        * Checks if user is creating for himself or manager is creating for user in league
        * Check if user already applied to post
        * Check if user already applied to game
        * Check if user even has visibility to apply for game
        * Check if game applied to is more than league advanced scheduling limit

    destroy: Destroy Application \n
    * Permissions: IsManager (of league application is assigned to)
    * Extra Notes:
        * Check if umpire: cannot canel within cancellation period

    list: List/Filter Application \n
    * Permissions: ApplicationFilterPermission
        * User Filter-Param is required
        * User must be same as request user

    cast: Cast Application to top of Order \n
    * Permissions: IsManager & IsApplicationLeague
    * Extra Notes:
        * Patch Request
    """
    queryset = Application.objects.all()
    serializer_classes = {
        'default': ApplicationRetrieveSerializer,
        'create': ApplicationCreateSerializer
    }
    permission_classes = (IsSuperUser | (
        permissions.IsAuthenticated & ActionBasedPermission),)
    action_permissions = {
        # create validation logic enforced on serializer
        permissions.IsAuthenticated: ["create"],
        # additional validation in destroy method
        IsApplicationLeague: ["destroy"],
        IsManager & IsApplicationLeague: ["cast"],
        ApplicationFilterPermission: ["list"]
    }
    filterset_class = ApplicationFilter

    @action(detail=True, methods=['patch'])
    def cast(self, request, pk):  # replace move order. Can only move application to top
        application = self.get_object()
        application.top()
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        cancellation_period = instance.post.game.division.league.cancellation_period
        if (instance.post.game.date_time - timezone.now()).days < cancellation_period:
            if not request.user.is_manager():
                return Response({"error": ' '.join(['cannot cancel within', str(cancellation_period), 'days'])}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
    permission_classes = (IsSuperUser | (
        permissions.IsAuthenticated & ActionBasedPermission),)
    action_permissions = {
        # manager of league requirement enforced on serializer level
        IsManager: ["create"],
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
    * Permission: GameFilterPermission (Can only filter division/division__in if accepted to all respective leagues, cannot list all games)
    * Query Params:
        * Division (either Division or Division__in is required)
        * Division__in (list of division pk's, queried using OR)
        * Date_time_before (iso format)
        * Date_time_after (iso format)
    """
    serializer_class = GameSerializer
    permission_classes = (IsSuperUser | (
        permissions.IsAuthenticated & ActionBasedPermission),)
    action_permissions = {
        # manager of league requirement enforced on serializer level
        IsManager: ["create"],
        IsGameLeague: ["retrieve"],
        IsManager & IsGameLeague: ["destroy"],
        (IsManager & (GameFilterDivisionManager | GameFilterDivisionInManager)) |
        GameFilterDivision | GameFilterDivisionIn | GameFilterUser: ["list"],
    }

    queryset = Game.objects.all()
    filterset_class = GameFilter
