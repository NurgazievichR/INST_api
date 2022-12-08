from django.shortcuts import get_object_or_404

from apps.post.models import Post

def has_permission_to_post(pk:int, request):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        ids = [i.to_user.id for i in request.user.subscriptions.filter(is_confirmed=True)]
        if post.user.id in ids or post.user == request.user or post.user.is_private == False:
            return True
        return False
    if post.user.is_private == False:
        return True
    return True