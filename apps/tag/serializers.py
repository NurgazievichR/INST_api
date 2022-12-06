from rest_framework import serializers

from apps.tag.models import Tag
from apps.post.models import Post


class PostFilterPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = super(PostFilterPrimaryKeyRelatedField, self).get_queryset()
        if not user or not queryset:
            return None
        return queryset.filter(user=user)

class TagSerializer(serializers.ModelSerializer):
    post = PostFilterPrimaryKeyRelatedField(queryset=Post.objects.all(), many=True)
    class Meta:
        model = Tag
        fields = '__all__'

    def create(self, validated_data):
        tags = Tag.objects.filter(title=validated_data['title'])
        if len(tags) == 0:
            return super().create(validated_data)
        for i in validated_data['post']:
            i.tags.add(tags[0]) 
        return tags[0]