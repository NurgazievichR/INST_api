from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.user.models import UserFollow

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'bio', 'avatar', 'email', 'date_joined', 'last_activity','password', 'edited_at',
        )
        read_only_fields = ('id', 'date_joined', 'last_activity')
        extra_kwargs = {'password': {'write_only': True, 'required':False}}
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.email = validated_data.get('email', instance.email)
        if validated_data.get('avatar'): 
            instance.avatar = validated_data.get('avatar', instance.avatar)
        if validated_data.get('password'):
            if len(validated_data.get('password')) > 7:
                instance.set_password(validated_data.get('password', instance.password))
            else:
                raise serializers.ValidationError({'password':'Пароль должен состовлять не менее 8 символов'})
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['subscriptions'] = instance.subscriptions.count()
        representation['subscribers'] = instance.subscribers.count()
        return representation

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True)
    password_repeat = serializers.CharField(max_length=255, write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'bio', 'avatar', 'email', 'password', 'password_repeat')

    def create(self, validated_data):
        password = validated_data['password']
        password_repeat = validated_data['password_repeat']
        if not len(password) > 7:
            raise serializers.ValidationError({'password':'Пароль должен состовлять не менее 8 символов'})
        if password == password_repeat:
            user = User.objects.create(
                username = validated_data['username'],
                first_name = validated_data['first_name'],
                last_name = validated_data['last_name'],
                bio = validated_data['bio'],
                avatar = validated_data['avatar'],
                email = validated_data['email'],
            )
            user.set_password(password)
            user.save()
            #VERIFICATION BY EMAIL
            return user
        raise serializers.ValidationError({'password':'Ваши пароли не совпадают'})


class UserFilterPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = super(UserFilterPrimaryKeyRelatedField, self).get_queryset()
        if not user or not queryset:
            return None
        return queryset.exclude(username=user.username)


class UserFollowSerializer(serializers.ModelSerializer):
    to_user = UserFilterPrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = UserFollow
        fields = ('id', 'from_user', 'to_user', 'create_at')
        read_only_fields = ('from_user', 'create_at')
