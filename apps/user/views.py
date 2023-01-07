from django.contrib.auth import get_user_model
from django.db import IntegrityError

from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.views import TokenObtainPairView as SimpleTokenObtainPairView


from apps.user.serializers import UserSerializer, UserCreateSerializer, UserFollowSerializer, TokenObtainPairSerializer, UserAcceptFollowRequestSerializer
from apps.user.models import UserFollow
from utils.permissions import IsAccountOwner, IsPrivateInf, IsFollowOwner, IsPrivateAccount, RequestFollowAcceptPermission
from apps.post.serializers import PostSerializer, LikeSerializer, SaveSerializer
from apps.comment.serializers import CommentChildSerializer
from apps.story.serializers import StorySerializer

User = get_user_model()

class TokenObtainPairView(SimpleTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAccountOwner(),)
    filter_backends = (SearchFilter,)
    search_fields = ['username']

    def get_permissions(self):
        if self.action in ['create']:
            return (AllowAny(),)
        return self.permission_classes

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserCreateSerializer
        return self.serializer_class

    @action(detail=True, methods=['get'], permission_classes= (IsPrivateAccount,))
    def posts(self, request, pk=None):
        user = self.get_object()
        posts = user.posts.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes= (IsPrivateAccount,))
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

    @action(detail=True, methods=['get'], permission_classes= (IsPrivateAccount,))
    def subscribers(self, request, pk=None):
        user = self.get_object()
        subscribers = user.subscribers.all()
        serializer = UserFollowSerializer(subscribers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes= (IsPrivateAccount,))
    def subscriptions(self, request, pk=None):
        user = self.get_object()
        subscriptions = user.subscriptions.all()
        serializer = UserFollowSerializer(subscriptions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=(IsPrivateInf,))
    def archives(self, request, pk=None):
        user = self.get_object()
        archives = user.stories.filter(is_archived=True)
        serializer = StorySerializer(archives, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes= (IsPrivateAccount,))
    def stories(self, request, pk=None):
        user = self.get_object()
        stories = user.stories.filter(is_archived=False)
        serializer = StorySerializer(stories, many=True)
        return Response(serializer.data)


class UserFollowViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = UserFollow.objects.all()
    serializer_class = UserFollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly(), IsFollowOwner())

    def get_permissions(self):
        if self.action in ['update']:
            return (RequestFollowAcceptPermission(),)
        return self.permission_classes

    def get_serializer_class(self):
        if self.action in ['update']:
            return UserAcceptFollowRequestSerializer
        return self.serializer_class


    def perform_create(self, serializer):
        to_user =  User.objects.get(pk=serializer.validated_data['to_user'].id)
        if to_user.is_private == False:
            serializer.save(is_confirmed=True, from_user=self.request.user)
        else:
            serializer.save(is_confirmed=False, from_user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
            # return Response({'fdfs':'dsgdsg'})
        except IntegrityError:
            return Response({'follow':'Вы не можете подписываться дважды'})


    @action(detail=False, methods=['get'], permission_classes= (IsPrivateAccount(),))
    def requests(self, request):
        follows = UserFollow.objects.filter(to_user=request.user, is_confirmed=False)
        serializer = UserFollowSerializer(follows, many=True)
        return Response(serializer.data)