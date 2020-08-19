from rest_framework import permissions, views
from rest_framework.response import Response

from backend.permissions import IsManager, IsSuperUser
from leagues.models import League
from teamsnap.models import TeamSnapNote, TeamSnapNoteItem
from teamsnap.teamsnap import TeamSnapBuilder

from .permissions import InLeague
from .serializers import TeamSnapNoteSerializer


class TeamSnapBuildView(views.APIView):
    permission_classes = (IsSuperUser | (
        permissions.IsAuthenticated & IsManager & InLeague), )

    def get_api_key(self, request, pk):
        api_key = request.query_params.get('api_key', None)
        league = League.objects.get(pk=pk)
        if api_key is None:
            api_key = league.api_key
        return api_key

    def get(self, request, pk, format=None):
        api_key = self.get_api_key(request, pk)
        if api_key == "":
            return Response({"error": "invalid api key"})
        ts = TeamSnapBuilder(api_key, League.objects.get(pk=pk))
        try:
            return Response(ts.build_tree())
        except:
            return Response({"error": "there was an unexpected error"})

    def post(self, request, pk, format=None):
        api_key = self.get_api_key(request, pk)
        if api_key == "":
            return Response({"error": "invalid api key"})
        ts = TeamSnapBuilder(api_key, League.objects.get(pk=pk))
        divisions = request.data.get('divisions', None)
        if divisions is None:
            return Response({"error": "must specify a list of division ts_ids"})
        try:
            ts.create_league(divisions)
        except:
            return Response({"error": "there was an unexpected error"})
        tsn = TeamSnapNote.objects.create(
            league=League.objects.get(pk=pk),
            note_type='build'
        )
        for exception_note in ts.exception_notes:
            TeamSnapNoteItem.objects.create(
                teamsnap_note=tsn,
                note=exception_note[:128]  # limit length
            )
        serializer = TeamSnapNoteSerializer(tsn)
        return Response(serializer.data)
