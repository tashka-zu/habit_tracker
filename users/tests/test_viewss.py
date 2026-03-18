from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationTest(APITestCase):
    def test_user_registration(self):
        """Проверка регистрации пользователя."""
        url = reverse("register")
        data = {
            "email": "test@example.com",
            "password": "testpass123",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "test@example.com")


class UserLoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )

    def test_user_login(self):
        """Проверка авторизации пользователя."""
        url = reverse("login")
        data = {
            "email": "test@example.com",
            "password": "testpass123",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
