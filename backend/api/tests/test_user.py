from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from api.tests.utils import (
    PROFILE_URL,
    REGISTER_URL,
)


class PublicUserTests(APITestCase):
    """
    Tests for an unauthenticated user.
    """
    def setUp(self):
        self.client = APIClient()

    def test_register_success(self):
        """
        Tests that user register successfully.
        """
        payload = {
            'username': 'testuser',
            'password': 'testpass',
        }

        res = self.client.post(REGISTER_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        users = get_user_model().objects.all()
        self.assertEqual(len(users), 1)

        user = users[0]
        self.assertEqual(user.username, payload['username'])


class UserTests(APITestCase):
    """
    Tests for the authenticated user.
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_profile(self):
        """
        Tests that user gets correct information in profile.
        """
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        fields = ['username', 'email', 'first_name', 'last_name']
        for field in fields:
            self.assertIn(field, res.data)
        self.assertNotIn('password', res.data)
