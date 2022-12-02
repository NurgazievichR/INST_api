from rest_framework import serializers

from apps.post.models import Post, PostImage, Save, Like

class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = '__all__'
    
    #a post can hold no more than 5 images
    def create(self, validated_data):
        post = validated_data['post']
        if len(post.post_images.all())==5:
            raise serializers.ValidationError({'max_error':'В одной публикации может быть только 5 изображений'})
        if not post.user == self.context['view'].request.user:
            raise serializers.ValidationError({'post':'Вы не можете добавлять картинки к посту, пользователь которого не вы'})
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    post_images = PostImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ('id','title','create_at','update_at','user','post_images')
        read_only_fields = ('update_at', 'user')

class SaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Save
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        save = Save.objects.filter(user=validated_data['user'], post=validated_data['post'])
        if len(save):
            raise serializers.ValidationError({'save':'Уже сохранённая публикация есть'})
        return super().create(validated_data)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ('user',)

    def create(self, validated_data):
        like = Like.objects.filter(user=validated_data['user'], post=validated_data['post'])
        if len(like):
            raise serializers.ValidationError({'save':'Этот пост уже лайкнут'})
        return super().create(validated_data)