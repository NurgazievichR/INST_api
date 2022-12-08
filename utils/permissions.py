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


class IsPrivateAccount(permissions.BasePermission):
    message = 'This is private account'
    def has_object_permission(self, request, view, obj):  
        if request.user.is_authenticated:
            if obj.is_private == True:
                if request.user == obj:
                    return True
                subs = obj.subscribers.all()
                subs2 = request.user.subscriptions.all()
                isFollowed = tuple(set(subs) & set(subs2))
                if isFollowed and isFollowed[0].is_confirmed == True:
                    return True
                return False
            return True
        if obj.is_private == False:
            return True
        return False


class RequestFollowAcceptPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.to_user == request.user and request.user.is_private == True:
            return True
        return False

