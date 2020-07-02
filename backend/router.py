from users.api.viewsets import UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet)

for url in router.urls:
    print(url)