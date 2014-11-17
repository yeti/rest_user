from mezzanine.core.auth_backends import MezzanineBackend

__author__ = 'baylee'


# TODO: shouldn't have Mezzanine dependencies
class CaseInsensitiveMezzanineBackend(MezzanineBackend):
    def authenticate(self, **kwargs):
        if kwargs.get("username", None):
            kwargs["username"] = kwargs.get("username", None).lower()
        if kwargs.get("email", None):
            kwargs["email"] = kwargs.get("email", None).lower()
        return super(CaseInsensitiveMezzanineBackend, self).authenticate(**kwargs)
