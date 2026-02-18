from django.test import TestCase
from habits.serializers import HabitSerializer
from habits.models import Habit
from django.contrib.auth import get_user_model

User = get_user_model()

class HabitSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_habit_serializer(self):
        data = {
            "place": "Дома",
            "time": "12:00:00",
            "action": "Выпить воду",
            "periodicity": 1,
            "duration": 60,
            "is_public": False,
        }
        serializer = HabitSerializer(data=data, context={'request': None})
        self.assertTrue(serializer.is_valid())
