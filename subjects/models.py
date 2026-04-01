from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL


class Subject(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  # <- allow null temporarily

    def __str__(self):
        return self.name


class Quiz(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="quizzes"
    )
    title = models.CharField(max_length=200)
    time_limit = models.PositiveIntegerField(default=10)  # minutes
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
