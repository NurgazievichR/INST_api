from django.urls import path

from rest_framework import routers

from apps.comment.views import CommentsViewSet

router = routers.DefaultRouter()
router.register('', CommentsViewSet, basename='comments')

urlpatterns = router.urls