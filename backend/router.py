from users.api.viewsets import UserViewSet, UserLeagueStatusViewSet
from leagues.api.viewsets import LeagueViewSet, RoleViewSet, DivisionViewSet, LevelViewSet
from games.api.viewsets import GameViewSet, PostViewSet, ApplicationViewSet
from notifications.api.viewsets import UmpCastNotificationViewSet, LeagueNotificationViewSet, GameNotificationViewSet, ApplicationNotificationViewSet
from teamsnap.api.viewsets import TeamSnapNoteViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('user-league-status', UserLeagueStatusViewSet,
                basename='user-league-status')
router.register('leagues', LeagueViewSet, basename='league')
router.register('divisions', DivisionViewSet, basename='division')
router.register('roles', RoleViewSet, basename='role')
router.register('levels', LevelViewSet, basename='level')
router.register('games', GameViewSet, basename='game')
router.register('posts', PostViewSet, basename='post')
router.register('applications', ApplicationViewSet, basename='application')
router.register('ump-cast-notifications',
                UmpCastNotificationViewSet, basename='ump-cast-notification')
router.register('league-notifications', LeagueNotificationViewSet,
                basename='league-notification')
router.register('game-notifications', GameNotificationViewSet,
                basename='game-notification')
router.register('application-notifications',
                ApplicationNotificationViewSet, basename='application-notification')
router.register('teamsnap-notes', TeamSnapNoteViewSet,
                basename='teamsnap-note')

for url in router.urls:
    print(url)
