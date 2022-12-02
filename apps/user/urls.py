from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.user.views import UserViewSet, current_user, current_user_saves

router = DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('current_user/', current_user, name='current_user'),
    path('current_user/saves', current_user_saves, name='current_user_saves'),
]

urlpatterns += router.urls