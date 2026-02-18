from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        """Проверка создания пользователя с email."""
        email = "test@example.com"
        password = "testpass123"
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Проверка нормализации email для новых пользователей."""
        email = "test@EXAMPLE.com"
        user = User.objects.create_user(email, "testpass123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Проверка создания пользователя с некорректным email."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="testpass123")

    def test_create_superuser(self):
        """Проверка создания суперпользователя."""
        user = User.objects.create_superuser(
            email="test@example.com", password="testpass123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
