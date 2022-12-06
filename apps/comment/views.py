from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.comment.models import Comment
from apps.comment.serializers import CommentSerializer
from utils.permissions import IsCommentOwnerOrPostOwner

class CommentsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsCommentOwnerOrPostOwner)

    def get_queryset(self):
        if self.action in ['list']:
            return super().get_queryset().filter(parent=None)
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        