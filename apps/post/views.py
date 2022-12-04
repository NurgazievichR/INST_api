from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.post.models import Post, PostImage, Save, Like
from apps.post.serializers import PostSerializer, PostImageSerializer, SaveSerializer, LikeSerializer
from apps.post.permissions import IsPostOwner, IsPostImageOwner
from apps.comment.models import Comment
from apps.comment.serializers import CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsPostOwner)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk):
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post, parent=None)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        likes = Like.objects.filter(post=post)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)


        
class PostImageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer      
    permission_classes = (IsPostImageOwner,)


class SaveViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Save.objects.all()
    serializer_class = SaveSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsPostOwner)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsPostOwner)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)