from django.contrib.auth import get_user_model
from rest_framework import serializers

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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'fullname', 'thumbnail')