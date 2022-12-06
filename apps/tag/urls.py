from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.tag.views import TagViewSet

router = DefaultRouter()
router.register('', TagViewSet, basename='tag')

urlpatterns = router.urls           