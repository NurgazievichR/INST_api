from rest_framework import viewsets, mixins, permissions

from utils.celery_tasks import archive_story
from apps.story.models import Story
from apps.story.serializers import StorySerializer
from utils.permissions import IsPostOwner


class StoryViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Story.objects.filter
    serializer_class = StorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsPostOwner)

    def get_queryset(self):
        stories = Story.objects.filter(user_id__in=[i.to_user.id for i in self.request.user.subscriptions.filter(is_confirmed=True)], is_archived=False).order_by('-create_at') | Story.objects.filter(user=self.request.user)
        return stories

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

