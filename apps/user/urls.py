from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.user.views import UserViewSet, UserFollowViewSet, current_user

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('follow', UserFollowViewSet, basename='follow')

urlpatterns = [
    path('current_user/', current_user, name='current_user'),
]

urlpatterns += router.urls