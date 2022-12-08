from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.user.views import UserViewSet, UserFollowViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('follow', UserFollowViewSet, basename='follow')


urlpatterns = router.urls