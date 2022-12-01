from django.urls import path
from rest_framework import routers

from apps.post.views import PostViewSet, PostImageViewSet

router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('images', PostImageViewSet, basename='images')

urlpatterns = router.urls