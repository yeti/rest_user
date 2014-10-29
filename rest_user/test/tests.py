import base64
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_core.rest_core.test import ManticomTestCase
from rest_user.rest_user.test.factories import UserFactory

__author__ = 'baylee'


User = get_user_model()


class UserTests(ManticomTestCase):
    def test_autocomplete(self):
        """
        Tests that when a string is sent with the user's name or username, we return a filtered list of users
        """
        url = reverse("users-list")
        bob = UserFactory(username="bob")
        frank = UserFactory(username="frank")
        UserFactory(username="mindy")
        parameters = {"search": "fra"}
        response = self.assertManticomGETResponse(url, parameters, "$userResponse", bob)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["username"], frank.username)


class AuthenticationTests(ManticomTestCase):
    def setUp(self):
        super(AuthenticationTests, self).setUp()
        self.user = User.objects.create_user(username='tester1', email='tester1@yetihq.com', password='password')

    def test_user_can_sign_up(self):
        url = reverse("sign_up")
        password = base64.encodestring("test")
        data = {
            "username": "tester",
            "email": "tester@yetihq.com",
            "password": password
        }
        self.assertManticomPOSTResponse(url, "$signUpRequest", "$signUpResponse", data, None)
        self.assertEqual(User.objects.filter(username="tester").count(), 1)

    def test_user_can_log_in(self):
        url = reverse("login")

        # With the correct username and password, a user can log in with basic auth
        auth_string = base64.encodestring("tester1:password")
        self.client.credentials(HTTP_AUTHORIZATION='Basic ' + auth_string)
        response = self.client.get(url)
        self.assertValidJSONResponse(response)
        self.check_response_data(response, "results", "$loginResponse")

        # Incorrect credentials return unauthorized
        auth_string = base64.encodestring("tester1:WRONGPASSWORD")
        self.client.credentials(HTTP_AUTHORIZATION='Basic ' + auth_string)
        response = self.client.get(url)
        self.assertHttpUnauthorized(response)

    def test_user_can_get_token(self):
        """
        Below is the test I want. But it fails because django-oauth-toolkit will only accept requests with
        content-type application/x-www-form-urlencoded. DRF does not appear to support this type.

        url = reverse("oauth2_provider:token")
        data = {
            "username": self.user.username,
            "email": self.user.email,
            "client_id": self.user.application_set.first().client_id,
            "client_secret": self.user.application_set.first().client_secret,
            "grant_type": "password"
        }
        self.assertManticomPOSTResponse(url, "$tokenRequest", "$tokenResponse", data, None)
        """
        pass

    def test_token_authenticates_user(self):
        pass
