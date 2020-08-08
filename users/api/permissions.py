from ..models import User, UserLeagueStatus
from rest_framework import permissions
from leagues.models import League


class IsUserOwner(permissions.BasePermission):
    """
    Check if request user owns profile or is viewing personal profile
    """

    def has_permission(self, request, view):
        if view.kwargs['pk'] == 'me':
            return True
        user = User.objects.get(pk=view.kwargs['pk'])
        return user == request.user


class IsLeagueMember(permissions.BasePermission):
    """
    Check if request user has valid user-list query scope.
    Must specify query param and be part of league
    """

    def has_permission(self, request, view):
        league_pk = request.query_params.get('league', None)
        if league_pk is not None and request.user.leagues.accepted().filter(pk=league_pk).exists():
            return True
        return False


class IsUserLeagueStatusOwner(permissions.BasePermission):
    """
    Check if request user is the owner of the UserLeagueStatus
    """

    def has_permission(self, request, view):
        return UserLeagueStatus.objects.filter(pk=view.kwargs['pk'], user=request.user).exists()


class IsUserLeagueStatusManager(permissions.BasePermission):
    """
    Check if request user is manager of the UserLeagueStatus
    """

    def has_permission(self, request, view):
        if not request.user.is_manager():
            return False
        if UserLeagueStatus.objects.get(pk=view.kwargs['pk']).league not in request.user.leagues.accepted():
            return False
        return True


class UserLeagueStatusFilterPermission(permissions.BasePermission):
    """
    UserLeagueStatus List-Filter Permissions
    * Umpires must filter by current user. League or no league is optional.
    * Managers can both apply to leagues and manage leagues. Permissions filtered accordingly
    """


    def has_permission(self, request, view):
        league_pk = request.query_params.get('league', None)
        user_pk = request.query_params.get('user', None)

        if request.user.is_umpire():  # must filter by user, any league or no league is ok
            if user_pk is None:
                return False
            if User.objects.get(pk=user_pk) != request.user:
                return False
            return True

        if request.user.is_manager():
            if user_pk is not None and league_pk is None:  # can only happen if manager is applying to league
                return User.objects.get(pk=user_pk) == request.user
            if user_pk is not None and league_pk is not None:  # manager applying to league OR manager managing player in league
                if User.objects.get(pk=user_pk) == request.user:
                    return True
                else:
                    return League.objects.get(pk=league_pk) in request.user.leagues.accepted()
            if user_pk is None and league_pk is None:  # no unrestricted access
                return False
            if user_pk is None and league_pk is not None:  # manager retrieving all ULS in league
                return League.objects.get(pk=league_pk) in request.user.leagues.accepted()

        return False
