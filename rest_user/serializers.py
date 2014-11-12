from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_core.rest_core.serializers import BaseModelSerializer

__author__ = 'baylee'


User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    client_id = serializers.SerializerMethodField('get_client_id')
    client_secret = serializers.SerializerMethodField('get_client_secret')

    class Meta:
        model = User
        fields = ('client_id', 'client_secret')

    def get_client_id(self, obj):
        return obj.application_set.first().client_id

    def get_client_secret(self, obj):
        return obj.application_set.first().client_secret


class SignUpSerializer(LoginSerializer):
    class Meta(LoginSerializer.Meta):
        fields = ('username', 'email', 'password', 'client_id', 'client_secret')
        write_only_fields = ('password',)


class UserSerializer(BaseModelSerializer):
    user_following_count = serializers.Field(source='user_following_count')
    user_followers_count = serializers.Field(source='user_followers_count')

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_active', 'is_admin', 'is_staff', 'is_superuser', 'groups',
                   'user_permissions')
