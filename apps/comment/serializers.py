from rest_framework import serializers

from apps.comment.models import Comment

class CommentSerializer(serializers.ModelSerializer):
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

