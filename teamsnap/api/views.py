from rest_framework import permissions, views
from rest_framework.response import Response

from backend.permissions import IsManager, IsSuperUser
from leagues.models import League
from teamsnap.models import TeamSnapNote, TeamSnapNoteItem
from teamsnap.teamsnap import TeamSnapBuilder, TeamSnapSyncer

from .permissions import InLeague
from .serializers import TeamSnapNoteSerializer


class TeamSnapBuildView(views.APIView):
    permission_classes = (IsSuperUser | (
        permissions.IsAuthenticated & IsManager & InLeague), )

    def get_api_key(self, pk):
        return League.objects.get(pk=pk).api_key

    def get(self, request, pk, format=None):
        api_key = self.get_api_key(pk)
        ts = TeamSnapBuilder(api_key, League.objects.get(pk=pk))
        if not ts.valid_key():
            return Response({"error": "invalid api key"})
        try:
            return Response(ts.build_tree())
        except:
            return Response({"error": "there was an unexpected error"})

    def post(self, request, pk, format=None):
        api_key = self.get_api_key(pk)
        ts = TeamSnapBuilder(api_key, League.objects.get(pk=pk))
        if not ts.valid_key():
            return Response({"error": "invalid api key"})
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


class TeamSnapSyncView(views.APIView):
    permission_classes = (IsSuperUser | (
        permissions.IsAuthenticated & IsManager & InLeague),)

    def get_api_key(self, pk):
        return League.objects.get(pk=pk).api_key

    def get(self, request, pk, format=None):
        api_key = self.get_api_key(pk)
        ts = TeamSnapSyncer(api_key, League.objects.get(pk=pk))
        if not ts.valid_key():
            return Response({"error": "invalid api key"})
        try:
            ts.sync()
        except:
            return Response({"error": "there was an unexpected error"})
        tsn = TeamSnapNote.objects.create(
            league=League.objects.get(pk=pk),
            note_type='sync'
        )
        for exception_note in ts.exception_notes:
            TeamSnapNoteItem.objects.create(
                teamsnap_note=tsn,
                note=exception_note[:128]
            )
        serializer = TeamSnapNoteSerializer(tsn)
        return Response(serializer.data)


class TeamSnapSaveKeyView(views.APIView):
    permission_classes = (IsSuperUser | (
        permissions.IsAuthenticated & IsManager & InLeague), )

    def get(self, request, pk, format=None):
        api_key = request.query_params.get('api_key', '')
        ts = TeamSnapSyncer(api_key, League.objects.get(pk=pk))
        league = League.objects.get(pk=pk)
        if not ts.valid_key():
            return Response({"status": "invalid"})
        else:
            league.api_key = api_key
            league.save()
            return Response({"status": "valid"})
