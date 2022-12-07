from rest_framework import serializers
from django.db.models import Q

from apps.comment.models import Comment
from apps.post.models import Post



class CommentFilterPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user.subscriptions.filter(is_confirmed=True)
        ids = [i.to_user.id for i in user]
        queryset = super(CommentFilterPrimaryKeyRelatedField, self).get_queryset()
        if not user or not queryset:
            return None
        return queryset.filter(Q(user_id__in=ids) | Q(user=self.context['request'].user))   


class CommentSerializer(serializers.ModelSerializer):
    post = CommentFilterPrimaryKeyRelatedField(queryset=Post.objects.all())
    replies = serializers.SerializerMethodField()

    def get_replies(self, obj):
        if not obj.parent is None:
            return False
        return CommentChildSerializer(Comment.objects.filter(parent=obj), many=True).data

    class Meta:
        model = Comment
        fields = ('id','body','post','user','date', 'parent', 'replies')
        read_only_fields = ('user',)        
    
    def create(self, validated_data):
        print('Test 1\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        if validated_data['parent']:
            validated_data['post'] = validated_data['parent'].post
            if validated_data['parent'].parent:
                validated_data['parent'] = validated_data['parent'].parent
        return super().create(validated_data)


class CommentChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','body','date','user')

class BaseCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body', 'post', 'user', 'date', 'parent')

