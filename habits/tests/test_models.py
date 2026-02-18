from django.test import TestCase
from django.contrib.auth import get_user_model
from habits.models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )

    def test_habit_creation(self):
        """Проверка создания привычки."""
        habit = Habit.objects.create(
            user=self.user,
            place="Дома",
            time="12:00:00",
            action="Выпить воду",
            is_pleasant=False,
            periodicity=1,
            duration=60,
            is_public=False,
        )

        self.assertEqual(habit.action, "Выпить воду")
        self.assertEqual(habit.duration, 60)

    def test_habit_validation(self):
        """Проверка валидации привычки."""
        with self.assertRaises(Exception):
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
            habit.clean()
