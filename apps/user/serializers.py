from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.user.models import UserFollow

User = get_user_model()


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': ('Активная учетная запись с указанными учетными данными не найдена')
    }

class UserSerializer(serializers.ModelSerializer):
    is_online = serializers.SerializerMethodField(source='is_online') 

    def get_is_online(self, obj):
        return obj.is_online() if obj.hide_status == False else False
        
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'bio', 'avatar', 'email', 'date_joined', 'last_activity', 'is_private','is_online', 'hide_status', 'password',
        )
        read_only_fields = ('id', 'date_joined', 'last_activity', 'is_online',)
        extra_kwargs = {'password': {'write_only': True, 'required':False}, 'hide_status':{'write_only':True}}
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.email = validated_data.get('email', instance.email)
        instance.is_private = validated_data.get('is_private', instance.is_private)
        instance.hide_status = validated_data.get('hide_status', instance.hide_status)
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
        if self.context['request'].user.is_authenticated:
            subs = instance.subscribers.all()
            subs2 = self.context['request'].user.subscriptions.all()
            isFollowed = tuple(set(subs) & set(subs2))
            representation['is_followed'] = True if isFollowed and isFollowed[0].is_confirmed == True else False
        representation['subscriptions'] = instance.subscriptions.filter(is_confirmed=True).count()
        representation['subscribers'] = instance.subscribers.filter(is_confirmed=True).count()
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
        fields = ('id', 'from_user', 'to_user', 'create_at', 'is_confirmed')
        read_only_fields = ('from_user', 'create_at', 'is_confirmed')

class UserAcceptFollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = ('id', 'from_user', 'create_at', 'is_confirmed')
        read_only_fields = ('id', 'from_user', 'create_at',)
        