from django.urls import path
from . import views

urlpatterns = [
    path("quiz/<int:quiz_id>/take/", views.take_quiz, name="take_quiz"),
    path("quiz/<int:quiz_id>/submit/", views.submit_quiz, name="submit_quiz"),
    path("quiz/<int:quiz_id>/retake/", views.retake_quiz, name="retake_quiz"),
]
