from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Count

from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from apps.user.serializers import UserSerializer, UserCreateSerializer, UserFollowSerializer
from apps.user.models import UserFollow
from apps.post.permissions import IsAccountOwner, IsPrivateInf, IsFollowOwner
from apps.post.serializers import PostSerializer, LikeSerializer, SaveSerializer
from apps.comment.serializers import CommentChildSerializer



User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAccountOwner,)

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserCreateSerializer
        return self.serializer_class

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        user = self.get_object()
        posts = user.posts.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        user = self.get_object()
        likes = user.liked.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=(IsPrivateInf,))
    def saves(self, request, pk=None):
        user = self.get_object()
        saves = user.saved.all()
        serializer = SaveSerializer(saves, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=(IsPrivateInf,))
    def comments(self, request, pk=None):
        user = self.get_object()
        comments = user.comments.all()
        serializer = CommentChildSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def subscribers(self, request, pk=None):
        user = self.get_object()
        subscribers = user.subscribers.all()
        serializer = UserFollowSerializer(subscribers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def subscriptions(self, request, pk=None):
        user = self.get_object()
        subscriptions = user.subscriptions.all()
        serializer = UserFollowSerializer(subscriptions, many=True)
        return Response(serializer.data)

    
@api_view(['GET'])
def current_user(request):
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    return Response({'Authentication Error':'You\'re not authenticated yet'})

class UserFollowViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = UserFollow.objects.all()
    serializer_class = UserFollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsFollowOwner)

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({'follow':'Вы не можете подписываться дважды'})
            