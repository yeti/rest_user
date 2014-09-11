from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics
from rest_framework.authentication import OAuth2Authentication
from rest_user.rest_user.serializers import SignUpSerializer, UserSerializer

__author__ = 'baylee'


User = get_user_model()


class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (OAuth2Authentication)
