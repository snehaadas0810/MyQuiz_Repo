from django.db import models
from subjects.models import Quiz


class Question(models.Model):
    QUESTION_TYPES = (
        ("mcq", "MCQ"),
        ("descriptive", "Descriptive"),
    )

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=20, choices=[("MCQ", "MCQ"), ("DESC", "Descriptive")]
    )

    option_a = models.CharField(max_length=255, blank=True, null=True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)

    correct_answer = models.TextField()
    marks = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text
