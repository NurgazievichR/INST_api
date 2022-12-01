from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.user.views import UserViewSet, current_user

router = DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('current_user/', current_user, name='current_user')
]

urlpatterns += router.urls