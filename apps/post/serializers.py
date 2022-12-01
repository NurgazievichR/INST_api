from rest_framework import serializers

from apps.post.models import Post, PostImage

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'
    
    #a post can hold no more than 5 images
    def create(self, validated_data):
        post = validated_data['post']
        if len(post.post_images.all())==5:
            raise serializers.ValidationError({'max_error':'В одной публикации может быть только 5 изображений'})
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    post_images = PostImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ('id','title','create_at','update_at','user','post_images')
        read_only_fields = ('update_at', 'user')

        
