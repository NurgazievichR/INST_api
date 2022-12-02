from django.urls import path
from rest_framework import routers

from apps.post.views import PostViewSet, PostImageViewSet, SaveViewSet, LikeViewSet

router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('images', PostImageViewSet, basename='images')
router.register('saves', SaveViewSet, basename='saves')
router.register('likes', LikeViewSet, basename='likes')

urlpatterns = router.urls