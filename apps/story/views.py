from rest_framework import viewsets, mixins, permissions

from utils.celery_tasks import archive_story
from apps.story.models import Story
from apps.story.serializers import StorySerializer
from apps.post.permissions import IsPostOwner


class StoryViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Story.objects.filter(is_archived=False)
    serializer_class = StorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsPostOwner)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_success_headers(self, data):
        archive_story.delay(id_story=data['id'])
        return super().get_success_headers(data)