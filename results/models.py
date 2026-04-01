from django.db import models
from django.conf import settings
from subjects.models import Quiz
from questions.models import Question

User = settings.AUTH_USER_MODEL


class Result(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    is_reviewed = models.BooleanField(default=False)
    is_pending_review = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.quiz}"


class StudentAnswer(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    selected_answer = models.CharField(max_length=200, blank=True)

    descriptive_answer = models.TextField(blank=True)

    is_correct = models.BooleanField(default=False)

    marks_awarded = models.IntegerField(default=0)

    is_reviewed = models.BooleanField(default=False)

    teacher_feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.result.student} - {self.question}"
