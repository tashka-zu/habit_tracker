from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from habits.models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpass")
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

    def test_habit_creation(self):
        self.assertEqual(self.habit.action, "Выпить воду")
        self.assertEqual(self.habit.duration, 60)

    def test_habit_validation(self):
        habit = Habit(
            user=self.user,
            place="Дома",
            time="12:00:00",
            action="Выпить воду",
            is_pleasant=False,
            periodicity=8,  # Ошибка: периодичность больше 7 дней
            duration=60,
            is_public=False,
        )
        with self.assertRaises(ValidationError):
            habit.clean()  # Ожидаем, что будет выброшено исключение ValidationError
