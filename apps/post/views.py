from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.post.models import Post, PostImage, Save, Like
from apps.post.serializers import PostSerializer, PostImageSerializer, SaveSerializer, LikeSerializer
from apps.post.permissions import IsPostOwner, IsPostImageOwner

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsPostOwner,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise serializers.ValidationError({'authentication':'Чтобы создать публикацию, вам нужно зарегистрироваться'})
        return super().create(request, *args, **kwargs)
        
class PostImageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer      
    permission_classes = (IsPostImageOwner,)


class SaveViewSet(viewsets.ModelViewSet):
    queryset = Save.objects.all()
    serializer_class = SaveSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsPostOwner)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsPostOwner)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)