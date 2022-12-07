from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count

from apps.post.models import Post, PostImage, Save, Like
from apps.post.serializers import PostSerializer, PostImageSerializer, SaveSerializer, LikeSerializer
from utils.permissions import IsPostOwner, IsPostImageOwner
from apps.comment.models import Comment
from apps.comment.serializers import CommentSerializer
from apps.tag.serializers import TagSerializer
from apps.tag.models import Tag
from utils.tools import has_permission_to_post

User = get_user_model()

class PostViewSet(viewsets.ModelViewSet):
    # .annotate(like_count=Count('liked')).order_by('-like_count')
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsPostOwner)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title']

    def get_queryset(self):
        posts = Post.objects.filter(user_id__in=[i.to_user.id for i in self.request.user.subscriptions.filter(is_confirmed=True)])
        posts_ = Post.objects.filter(user__is_private=False).exclude(user=self.request.user)
        qr = posts | posts_
        qr = qr | Post.objects.filter(user=self.request.user)
        qr = qr.annotate(like_count=Count('liked')).order_by('-like_count')
        return qr

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk):
        if has_permission_to_post(pk, request=request):
            post = get_object_or_404(Post, pk=pk)
            comments = Comment.objects.filter(post=post, parent=None)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        return Response({'Error':'Не можете просматривать комментарии, так как приватный аккаунт'})

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        if has_permission_to_post(pk, request=request):
            post = get_object_or_404(Post, pk=pk)
            likes = Like.objects.filter(post=post)
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data)
        return Response({'Error':'Не можете просматривать лайки, так как приватный аккаунт'})

    @action(detail=True, methods=['get'])
    def tags(self, request, pk=None):
        if has_permission_to_post(pk, request=request):
            post = get_object_or_404(Post, pk=pk)
            tags = Tag.objects.filter(post=post)
            serializer = TagSerializer(tags, many=True)
            return Response(serializer.data)
        return Response({'Error':'Не можете просматривать тэги, так как приватный аккаунт'})
        
class PostImageViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
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

