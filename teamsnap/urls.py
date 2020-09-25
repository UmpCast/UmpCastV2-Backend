from django.urls import path

from .api.views import TeamSnapBuildView, TeamSnapSyncView, TeamSnapSaveKeyView

urlpatterns = [
    path('<int:pk>/build/', TeamSnapBuildView.as_view(), name='teamsnap-build'),
    path('<int:pk>/sync/', TeamSnapSyncView.as_view(), name='teamsnap-sync'),
    path('<int:pk>/save/', TeamSnapSaveKeyView.as_view(), name='teamsnap-save')
]
