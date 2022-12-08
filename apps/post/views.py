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
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsPostOwner)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title']

    def get_queryset(self):

        #Если пользователь авторизован:
            # 1. Берет посты пользователей на который он подписан, и принят
            # 2. Берет посты пользоваттелей открытых аккаунтов
            # 3. Берет посты самого авторизованного пользователя
            # И выводит всех по количеству лайков
        # Если пользователь не авторизован
            # 1. Берет посты пользоваттелей открытых аккаунтов и выводит по количеству лайков

        if self.request.user.is_authenticated:
            posts = Post.objects.filter(user_id__in=[i.to_user.id for i in self.request.user.subscriptions.filter(is_confirmed=True)])
            posts_ = Post.objects.filter(user__is_private=False).exclude(user=self.request.user)
            qr = posts | posts_ | Post.objects.filter(user=self.request.user)
            qr = qr.annotate(like_count=Count('liked')).order_by('-like_count')
            return qr
        posts_ = Post.objects.filter(user__is_private=False).annotate(like_count=Count('liked')).order_by('-like_count')
        return posts_

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    #Вывод комментариев, лайков и тегов поста
    # Если пользователь авторизован
        # 1. Если у автора поста открытый аккаунт, то пользователь может просматривать данные
        # 2. Если у автора закрытый аккаунт, и пользователь подписан, то может просматривать
        # 3. Если автором постов является сам пользователь, может
        # 4. Если пользователь не подписан на автора с закрытым аккаунтом, то не может просмтаривать
    # Если пользователь не авторизован
        # 1. Если у автора поста открытый аккаунт

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
    permission_classes = (IsAuthenticatedOrReadOnly, IsPostImageOwner)


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

