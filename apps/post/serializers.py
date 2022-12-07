from rest_framework import serializers
from django.db.models import Q

from apps.post.models import Post, PostImage, Save, Like
from apps.tag.serializers import TagSerializer


class PostImageFilterPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = super(PostImageFilterPrimaryKeyRelatedField, self).get_queryset()
        if not user or not queryset:
            return None
        return queryset.filter(user=user)



class PostImageSerializer(serializers.ModelSerializer):
    post = PostImageFilterPrimaryKeyRelatedField(queryset=Post.objects.all())
    class Meta:
        model = PostImage
        fields = '__all__'
    
    #a post can hold no more than 5 images
    def create(self, validated_data):
        post = validated_data['post']
        if len(post.post_images.all())==5:
            raise serializers.ValidationError({'max_error':'В одной публикации может быть только 5 изображений'})
        return super().create(validated_data)








class SaveFilterPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user.subscriptions.filter(is_confirmed=True)
        ids = [i.to_user.id for i in user]
        queryset = super(SaveFilterPrimaryKeyRelatedField, self).get_queryset()
        if not user or not queryset:
            return None
        return queryset.filter(Q(user_id__in=ids) | Q(user=self.context['request'].user))   


class SaveSerializer(serializers.ModelSerializer):
    post = SaveFilterPrimaryKeyRelatedField(queryset = Post.objects.all())
    class Meta:
        model = Save
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        save = Save.objects.filter(user=validated_data['user'], post=validated_data['post'])
        if len(save):
            raise serializers.ValidationError({'save':'Уже сохранённая публикация есть'})
        return super().create(validated_data)


class LikeFilterPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user.subscriptions.filter(is_confirmed=True)
        ids = [i.to_user.id for i in user]
        queryset = super(LikeFilterPrimaryKeyRelatedField, self).get_queryset()
        if not user or not queryset:
            return None
        return queryset.filter(Q(user_id__in=ids) | Q(user=self.context['request'].user))  


class LikeSerializer(serializers.ModelSerializer):
    post = LikeFilterPrimaryKeyRelatedField(queryset=Post.objects.all())
    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ('user',)

    def create(self, validated_data):
        like = Like.objects.filter(user=validated_data['user'], post=validated_data['post'])
        if len(like):
            raise serializers.ValidationError({'save':'Этот пост уже лайкнут'})
        return super().create(validated_data)




class PostSerializer(serializers.ModelSerializer):
    post_images = PostImageSerializer(many=True, read_only=True)
    liked = LikeSerializer(many=True, read_only=True) 

    class Meta:
        model = Post
        fields = ('id','title','create_at','update_at','user','post_images','liked',)
        read_only_fields = ('update_at', 'user')
