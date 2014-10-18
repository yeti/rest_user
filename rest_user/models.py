from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, is_admin, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        user = self.model(username=username, email=email, is_staff=is_staff,
                          is_active=True, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True, True, **extra_fields)


class AbstractYeti(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=80, unique=True)
    # Field name should be `fullname` instead of `full_name` for python-social-auth
    fullname = models.CharField(max_length=80, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    original_photo = models.ImageField(upload_to="user_photos/original/", blank=True, null=True)
    small_photo = models.ImageField(upload_to="user_photos/small/", blank=True, null=True)
    large_photo = models.ImageField(upload_to="user_photos/large/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="user_photos/thumbnail/", blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"%s" % self.username
