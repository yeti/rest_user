import base64
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import viewsets, generics, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_core.rest_core.permissions import IsOwnerOrReadOnly, IsOwner
from rest_user.rest_user.permissions import IsAuthenticatedOrCreate
from rest_user.rest_user.serializers import SignUpSerializer, UserSerializer, LoginSerializer, PasswordSerializer

__author__ = 'baylee'


User = get_user_model()


class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)


class Login(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    authentication_classes = (BasicAuthentication,)

    def get_queryset(self):
        return [self.request.user]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    search_fields = ('username', 'fullname')

    @list_route(methods=["get"])
    def me(self, request):
        if request.user.is_authenticated():
            serializer = self.get_serializer(instance=request.user)
            return Response(serializer.data)
        else:
            return Response({"errors": "User is not authenticated"}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['patch'])
    def password(self, request, pk=None):
        user = self.get_object()
        if not user.check_password(base64.decodestring(request.DATA['old_password'])):
            raise APIException("Old password does not match")
        serializer = PasswordSerializer(data=request.DATA)
        if serializer.is_valid():
            user.set_password(base64.decodestring(serializer.data['password']))
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = PasswordSerializer
    permission_classes = (IsOwner,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        self.object = self.get_object_or_none()

        # Once the serializer is called, the object becomes the updated version of the object. To access the original
        # version of the user object to check password, we override the entire update method
        if not request.DATA.get('old_password', None):
            raise APIException("Must provide old password")
        elif not request.DATA.get('password', None):
            raise APIException("Must provide new password")
        if not self.object.check_password(base64.decodestring(request.DATA['old_password'])):
            raise APIException("Old password does not match")

        serializer = self.get_serializer(self.object, data=request.DATA,
                                         files=request.FILES, partial=partial)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.pre_save(serializer.object)
        except ValidationError as err:
            # full_clean on model instance may be called in pre_save,
            # so we have to handle eventual errors.
            return Response(err.message_dict, status=status.HTTP_400_BAD_REQUEST)

        if self.object is None:
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        self.object = serializer.save(force_update=True)
        self.post_save(self.object, created=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
