from rest_framework import serializers
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions 
from django.shortcuts import get_object_or_404

from apps.tag.models import Tag
from apps.tag.serializers import TagSerializer
from apps.post.models import Post
from apps.post.serializers import PostSerializer

class TagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        tag = get_object_or_404(Tag, pk=pk)
        posts = [i for i in tag.post.all()]
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

