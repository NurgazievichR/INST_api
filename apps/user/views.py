from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.user.serializers import UserSerializer, UserCreateSerializer
from apps.post.permissions import IsAccountOwner


User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAccountOwner,)

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserCreateSerializer
        return self.serializer_class

    #Favorites

    


@api_view(['GET'])
def current_user(request):
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    return Response({'Authentication Error':'You\'re not authenticated yet'})