from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from habits.models import Habit

User = get_user_model()


class HabitAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        refresh = RefreshToken.for_user(cls.user)
        cls.access_token = str(refresh.access_token)

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_get_habits(self):
        """Проверка получения списка привычек."""
        url = reverse("habit-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_habit(self):
        """Проверка создания привычки."""
        url = reverse("habit-list")
        data = {
            "place": "На работе",
            "time": "18:00:00",
            "action": "Сделать зарядку",
            "periodicity": 1,
            "duration": 60,
            "is_public": False,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 1)
