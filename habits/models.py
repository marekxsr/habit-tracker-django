from django.db import models
from django.contrib.auth.models import User


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100)

    description = models.CharField(
        max_length=255,
        blank=True
    )

    streak = models.PositiveIntegerField(default=0)

    completed_today = models.BooleanField(default=False)

    last_completed_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class HabitCompletion(models.Model):
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="completions"
    )

    date = models.DateField()

    class Meta:
        unique_together = ("habit", "date")

    def __str__(self):
        return f"{self.habit.title} - {self.date}"