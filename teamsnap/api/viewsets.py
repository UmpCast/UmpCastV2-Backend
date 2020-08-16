from rest_framework import viewsets, mixins
from ..models import TeamSnapNote
from .serializers import TeamSnapNoteSerializer
from backend.permissions import IsManager, IsSuperUser
from rest_framework import permissions
from .permissions import TeamSnapNoteFilterPermission


class TeamSnapNoteViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = TeamSnapNote.objects.all()
    filter_fields = ('league',)
    serializer_class = TeamSnapNoteSerializer
    permission_classes = (IsSuperUser | (permissions.IsAuthenticated & IsManager & TeamSnapNoteFilterPermission), )    
