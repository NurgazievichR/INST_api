from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.story.models import Story

User = get_user_model()

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'
        read_only_fields = ('create_at', 'user', 'is_archived')

    def create(self, validated_data):
        if len(validated_data['user'].stories.all()) == 30:
            raise serializers.ValidationError({'story':'Сторисов не может быть больше тридцати'})   
        return super().create(validated_data)