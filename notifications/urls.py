from django.urls import path
from .api.views import NotificationListView

urlpatterns = [
    path('<int:pk>/', NotificationListView.as_view(), name='notification-list')
]
