from .serializers import (
    LeaguePrivateSerializer,
    LeaguePublicSerializer,
    DivisionSerializer,
    RoleSerializer,
    ApplyLeagueCodeSerializer
)

from .permissions import (
    IsManager, IsCodeOwner, ListCodePermission,
    IsRoleOwner, IsDivisionOwner, IsUmpireOwner, IsLeagueOwner
)

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from backend.permissions import ActionBasedPermission
from drf_multiple_serializer import ActionBaseSerializerMixin
from ..models import League, Division, Role, ApplyLeagueCode


class ApplyLeagueCodeViewSet(viewsets.ModelViewSet):
    queryset = ApplyLeagueCode.objects.all()
    filter_fields = ('league', )
    serializer_class = ApplyLeagueCodeSerializer
    permission_classes = (ActionBasedPermission, )
    action_permissions = {
        IsManager: ['create'],  # league validated on serializer level
        IsCodeOwner: ['retrieve', 'update', 'partial_update', 'destroy'],
        ListCodePermission: ['list']
    }

    # @action(detail=True, methods=['post'])
    # def validate_code(self, request):
    #     code = request.data.get('code', None)
    #     if code is None:
    #         return Response({"error": "missing parameeters"}, status=status.HTTP_400_BAD_REQUEST)
    #     if ApplyLeagueCode.objects.filter(code=code).exists():
    #         return Response()
    #     else:
    #         return Response({"ApplyLeagueCode": ["invalid code"]}, status=status.HTTP_400_BAD_REQUEST)
        # code_object = ApplyLeagueCode.objects.ge


class RoleViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (ActionBasedPermission, )
    action_permissions = {
        IsManager: ['create'],  # league validated on serializer level
        IsRoleOwner: ['destroy']
    }


class DivisionViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    permission_classes = (ActionBasedPermission, )
    action_permissions = {
        IsManager: ['create'],  # league validated on serializer level
        IsDivisionOwner: ['destroy']
    }


class LeagueViewSet(ActionBaseSerializerMixin, viewsets.ModelViewSet):
    queryset = League.objects.all()
    filter_fields = ('user', )
    serializer_classes = {
        'default': LeaguePrivateSerializer,
        'list': LeaguePublicSerializer
    }
    permission_classes = (ActionBasedPermission, )
    action_permissions = {
        IsManager: ['create'],
        IsUmpireOwner: ['list'],
        IsLeagueOwner: ['update', 'partial_update', 'retrieve', 'destroy']
    }
