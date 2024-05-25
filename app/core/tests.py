from unittest.mock import patch

from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from app.core.models import User


class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.group = Group.objects.create(name="admins")
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="adminpass",
            email="admin@example.com",
            groups=self.group,
        )
        self.token, _ = Token.objects.get_or_create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    @patch("app.core.tasks.on_user_created.delay", return_value=None)
    def test_create_user(self, mock_on_user_created):
        url = reverse("users")
        data = {
            "username": "testuser",
            "password": "password",
            "email": "admin2@example.com",
        }
        response = self.client.post(url, data, format="json")

        # Assert function was called once
        mock_on_user_created.assert_called_once()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_users(self):
        url = reverse("users")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detail(self):
        user = User.objects.create_user(
            username="testuser",
            password="password",
            groups=self.group,
            email="user1@example.com",
        )
        url = reverse("user-detail", kwargs={"pk": user.pk})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        user = User.objects.create_user(
            username="testuser",
            password="password",
            groups=self.group,
            email="user2@example.com",
        )
        url = reverse("user-detail", kwargs={"pk": user.pk})
        data = {"username": "updateduser"}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        user = User.objects.create_user(
            username="testuser",
            password="password",
            groups=self.group,
        )
        url = reverse("user-detail", kwargs={"pk": user.pk})
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LoginTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.group = Group.objects.create(name="tests")
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
            email="admin2@example.com",
            groups=self.group,
        )

    def test_login(self):
        url = reverse("login")
        data = {"username": "testuser", "password": "password"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_invalid_credentials(self):
        url = reverse("login")
        data = {"username": "wronguser", "password": "wrongpass"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
