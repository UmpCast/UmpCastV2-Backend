from users.api.viewsets import UserViewSet, UserLeagueStatusViewSet
from leagues.api.viewsets import LeagueViewSet, ApplyLeagueCodeViewSet, RoleViewSet, DivisionViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('user-league-status', UserLeagueStatusViewSet, basename='user-league-status')
router.register('leagues', LeagueViewSet, basename='league')
router.register('divisions', DivisionViewSet, basename='division')
router.register('roles', RoleViewSet, basename='role')
router.register('apply-league-code', ApplyLeagueCodeViewSet, basename='apply-league-code')


for url in router.urls:
    print(url)
