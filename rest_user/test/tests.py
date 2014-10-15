from django.core.urlresolvers import reverse
from rest_core.rest_core.test import ManticomTestCase
from rest_user.rest_user.test.factories import UserFactory

__author__ = 'baylee'


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
