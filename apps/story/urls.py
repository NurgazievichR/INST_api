from rest_framework.routers import DefaultRouter

from apps.story.views import StoryViewSet

router = DefaultRouter()
router.register('', StoryViewSet, basename='stories')

urlpatterns = router.urls