from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from habits.models import Habit

User = get_user_model()


class HabitAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpass")
        refresh = RefreshToken.for_user(cls.user)
        cls.access_token = str(refresh.access_token)
        cls.habit = Habit.objects.create(
            user=cls.user,
            place="Дома",
            time="12:00:00",
            action="Выпить воду",
            is_pleasant=False,
            periodicity=1,
            duration=60,
            is_public=False,
        )

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_get_habits(self):
        response = self.client.get("/api/habits/")
        self.assertEqual(response.status_code, 200)

    def test_create_habit(self):
        data = {
            "place": "На работе",
            "time": "18:00:00",
            "action": "Сделать зарядку",
            "periodicity": 1,
            "duration": 60,
            "is_public": False,
        }
        response = self.client.post("/api/habits/", data, format="json")
        print(response.data)  # Вывод для диагностики
        self.assertEqual(response.status_code, 201)
