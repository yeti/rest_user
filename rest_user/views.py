import base64
from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics
from rest_framework.authentication import BasicAuthentication
from rest_user.rest_user.permissions import IsAuthenticatedOrCreate
from rest_user.rest_user.serializers import SignUpSerializer, UserSerializer, LoginSerializer

__author__ = 'baylee'


User = get_user_model()


class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)

    def post_save(self, obj, created=False):
        """
        On creation, decode the base64 password passed up and replace with a hashed version.
        """
        if created:
            password = base64.decodestring(obj.password)
            obj.set_password(password)
            obj.save()


class Login(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    authentication_classes = (BasicAuthentication,)

    def get_queryset(self):
        return [self.request.user]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
