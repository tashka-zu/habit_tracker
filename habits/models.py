from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class Habit(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    place = models.CharField(max_length=200, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=200, verbose_name="Действие")
    is_pleasant = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
    )
    periodicity = models.PositiveIntegerField(
        default=1, verbose_name="Периодичность (в днях)"
    )
    reward = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Вознаграждение"
    )
    duration = models.PositiveIntegerField(
        default=120, verbose_name="Время на выполнение (в секундах)"
    )
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    def clean(self):
        if self.related_habit and self.reward:
            raise ValidationError(
                "Нельзя одновременно указывать связанную привычку и вознаграждение."
            )

        if self.duration > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        if self.periodicity > 7:
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")

    def __str__(self):
        return f"{self.user} будет {self.action} в {self.time} в {self.place}"
