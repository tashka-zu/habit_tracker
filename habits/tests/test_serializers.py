from django.test import TestCase
from django.contrib.auth import get_user_model
from habits.serializers import HabitSerializer
from habits.models import Habit

User = get_user_model()


class HabitSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )

    def test_habit_serializer(self):
        """Проверка сериализатора привычки."""
        data = {
            "place": "Дома",
            "time": "12:00:00",
            "action": "Выпить воду",
            "periodicity": 1,
            "duration": 60,
            "is_public": False,
        }
        serializer = HabitSerializer(data=data, context={"request": None})
        self.assertTrue(serializer.is_valid())
