from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserAuthFlowTests(APITestCase):
    def test_register_login_and_get_user_info(self):
        register_payload = {
            "email": "alice@example.com",
            "password": "StrongPass123",
            "password_confirm": "StrongPass123",
            "first_name": "Alice",
            "last_name": "Martin",
            "phone": "0340000000",
            "role": "CLIENT",
        }

        register_response = self.client.post(reverse("register"), register_payload, format="json")
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(register_response.data["email"], register_payload["email"])

        login_response = self.client.post(
            reverse("login"),
            {"email": register_payload["email"], "password": register_payload["password"]},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", login_response.data)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access_token']}")
        user_info_response = self.client.get(reverse("user_info"))

        self.assertEqual(user_info_response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_info_response.data["email"], register_payload["email"])

    def test_login_fails_with_wrong_password(self):
        user = User.objects.create_user(
            email="bob@example.com",
            password="RightPass123",
            first_name="Bob",
            last_name="Ranaivo",
            is_active=True,
            email_verified=True,
        )
        self.assertTrue(user.check_password("RightPass123"))

        response = self.client.post(
            reverse("login"),
            {"email": "bob@example.com", "password": "WrongPass999"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_info_requires_authentication(self):
        response = self.client.get(reverse("user_info"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
