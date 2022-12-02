from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from apps.user.serializers import UserSerializer, UserCreateSerializer
from apps.post.permissions import IsAccountOwner
from apps.post.serializers import PostSerializer, LikeSerializer, SaveSerializer


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

    


@api_view(['GET'])
def current_user(request):
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    return Response({'Authentication Error':'You\'re not authenticated yet'})

@api_view(['GET'])
def current_user_saves(request):
    user = request.user
    saves = user.saved.all()
    serializer = SaveSerializer(saves, many=True)
    return Response(serializer.data)
