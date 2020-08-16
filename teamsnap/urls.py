from django.urls import path
from .api.views import TeamSnapBuildView

urlpatterns = [
    path('<int:pk>/build/', TeamSnapBuildView.as_view(), name='teamsnap-build')
]
