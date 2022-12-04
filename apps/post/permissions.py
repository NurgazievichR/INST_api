from rest_framework import permissions


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj): 
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user == obj:
            return True
        return False


class IsPostOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):    
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user == obj.user:
            return True
        return False

class IsPostImageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):    
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user == obj.post.user:
            return True
        return False

class IsCommentOwnerOrPostOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user == obj.user:
            return True 
        if request.user == obj.post.user:
            return True
        return False

class IsPrivateInf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        return False


class IsFollowOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.from_user == request.user or obj.to_user == request.user:
            return True 
        return False