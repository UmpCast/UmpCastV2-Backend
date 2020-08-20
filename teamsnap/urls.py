from django.urls import path

from .api.views import TeamSnapBuildView, TeamSnapSyncView

urlpatterns = [
    path('<int:pk>/build/', TeamSnapBuildView.as_view(), name='teamsnap-build'),
    path('<int:pk>/sync/', TeamSnapSyncView.as_view(), name='teamsnap-sync')
]
